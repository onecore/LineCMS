"""
KnightSolutions Canada
Extendable Content Manage System for any Website template
www.KnightStudio.ca - KnightStudio Dashboard / Client files
Aug 31,2023
www.sinsoro.com - SinsoroCMS / Client files
Sept 19, 2023
Developed by Mark Anthony Pequeras - Python >= v3
Database: Sqlite3
"""

import dataengine
import os
from flask import Flask, Blueprint, g, flash, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flask_ckeditor import CKEditor
from flask_paginate import Pagination, get_page_parameter
import templater as temple
import renderfunc as rf
from enginepublic import loaders
from flask_mail import Mail, Message

# Dashboard imports/views
from engine.blog import blog
from engine.api import api
from engine.uploader import uploader
from engine.product import product
from engine.modules import module
from engine.dashboard import dashboard
from engine.account import account
from engine.message import message
from engine.login import logins
from engine.other import other
import dataengine
# Dashboard imports/views

# Public views
from enginepublic.product import productuser
from enginepublic.blog import bloguser
from enginepublic.main import mains
from enginepublic.notfound import notfound
# Public views

ckeditor = CKEditor()
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'svg', 'ico'])
version = "1.4"
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

ckeditor.init_app(app)  # wysiwyg html editor

UPLOAD_FOLDER = 'static/dashboard/uploads'
UPLOAD_FOLDER_PRODUCTS = 'static/dashboard/uploads/products'
UPLOAD_FOLDER_BLOG = 'static/dashboard/uploads/blog'
app.secret_key = '\xb2\xcb\x06\x85\xb1\xcfZ\x9a\xcf\xb3h\x13\xf6\xa6\xda)\x7f\xdd\xdb\xb2BK>'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Mail Infos below
__de = dataengine.knightclient()
mailinfo = __de.productsettings_get()
logger = __de.log
try:
    maildata = eval(mailinfo[13])
    app.config['MAIL_SERVER']= maildata['server']
    app.config['MAIL_PORT'] = int(maildata['port'])
    app.config['MAIL_USERNAME'] = maildata['email']
    app.config['MAIL_PASSWORD'] = maildata['password']
    app.config['MAIL_USE_TLS'] = True if maildata['tls'] == "YES" else False
    app.config['MAIL_USE_SSL'] =  True if maildata['ssl'] == "YES" else False
    logger(f"Mail SMTP settings/credentials Loaded")

except Exception as e:
    logger(f"Error -> {e}")
    

mail = Mail(app)


@app.route("/test-mail",methods=["POST"])
def sendmail_test():
    if request.method == "POST":
        subject = 'Test Email!'
        message = '<b>Hello from KnightStudio</b>'
        if request.data:
            r = eval(request.data)
            msg = Message(
                subject=subject,
                recipients=[r['receiver']],
                html=message,
                sender=app.config['MAIL_USERNAME'],
            )
            try:
                mail.send(msg)
                return jsonify({"status":1,"message":"Email sent without any error"})
            except Exception as e:
                return jsonify({"status":0,"message":f"Error occured: {e}"})


def sendmail(data):
    msg = Message(
        subject=data['subject'],
        recipients=[data['reciever']],
        html=data['message'],
        sender=data['sender'],
    )
    try:
        mail.send(msg)
        return jsonify({"status":1,"message":"Email sent without any error"})
    except Exception as e:
        logger(f"Mail send failed, {e}")
        return jsonify({"status":0,"message":f"Error occured: {e}"})



"""
Blueprinted routes
"""
# Dashboard
app.register_blueprint(blog)
app.register_blueprint(api)
app.register_blueprint(uploader)
app.register_blueprint(product)
app.register_blueprint(module)
app.register_blueprint(dashboard)
app.register_blueprint(account)
app.register_blueprint(message)
app.register_blueprint(logins)
app.register_blueprint(other)
# Dashboard

# User
app.register_blueprint(productuser)
app.register_blueprint(bloguser)
app.register_blueprint(mains)
app.register_blueprint(notfound)
# User



"""
functions for Jinja templating (Dashboard)
"""
app.jinja_env.globals.update(blog_list_badge_category=rf.ks_badge_insert)
app.jinja_env.globals.update(admin_button=rf.ks_include_adminbutton)
app.jinja_env.globals.update(khtml2text=rf.ks_html2text)
app.jinja_env.globals.update(khtml2text_truncate=rf.ks_html2text_truncate)
app.jinja_env.globals.update(ks_tolist=rf.ks_tolist)
app.jinja_env.globals.update(ks_getdictkeys=rf.ks_getdictkeys)
app.jinja_env.globals.update(ks_tojson=rf.ks_tojson)
app.jinja_env.globals.update(ks_variantcount=rf.ks_variantcount)
app.jinja_env.globals.update(ks_todict=rf.ks_todict)

"""
functions for Jinja templating (Public)
"""
app.jinja_env.globals.update(loadblogs=loaders.loadblogs)
app.jinja_env.globals.update(loadproducts=loaders.loadproducts)
app.jinja_env.globals.update(loaddate=loaders.dateformatter)
