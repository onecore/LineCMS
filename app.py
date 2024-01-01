"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
from helpers.settingsvalidate import svalidate

# Remove this code if you want to.
if not svalidate():
    print("\nSandCMS: Error in Settings file Detected, Please fix to prevent future errors\n")
else:
    print("\nSandCMS: Settings loaded\n")
# Remove this code if you want to.

    
import dataengine
import helpers.templateparser as rf
from flask import Flask, request, jsonify,request
from flask_ckeditor import CKEditor
from helpers import checkpoint
from enginepublic import loaders
from flask_mail import Mail, Message
from ast import literal_eval as lite
from helpers import dataparser

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
from engine.editor import editor
from engine.install import install
# Dashboard imports/views

# Public views
from enginepublic.main import mains
from enginepublic.blog import bloguser
from enginepublic.product import productuser
from enginepublic.notfound import notfound
from enginepublic.extra import extra
# Public views

version = "1.4"
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

ckeditor = CKEditor()
ckeditor.init_app(app)  # wysiwyg html editor
app.secret_key = '\xb2\xcb\x06\x85\xb1\xcfZ\x9a\xcf\xb3h\x13\xf6\xa6\xda)\x7f\xdd\xdb\xb2BK>'

__de = dataengine.SandEngine()
mailinfo = __de.productsettings_get()
logger = __de.log 

try:
    maildata = lite(mailinfo[13])
    app.config['MAIL_SERVER']= maildata['server']
    app.config['MAIL_PORT'] = int(maildata['port'])
    app.config['MAIL_USERNAME'] = maildata['email']
    app.config['MAIL_PASSWORD'] = maildata['password']
    app.config['MAIL_USE_TLS'] = True if maildata['tls'] == "YES" else False
    app.config['MAIL_USE_SSL'] =  True if maildata['ssl'] == "YES" else False
    logger(f"SandCMS: Mail SMTP settings/credentials Loaded")
    print("SandCMS: Mail SMTP settings/credentials Loaded\n")

except Exception as e:
    logger(f"SandCMS: Mail Error -> {e}")
    print("\nSandCMS: SMTP Settings loaded\n")

mail = Mail(app)


@app.route("/test-mail",methods=["POST"])
@checkpoint.onlylogged
def sendmail_test():
    if request.method == "POST":
        subject = 'Test Email!'
        message = '<b>Hello from KnightStudio</b>'
        if request.data:
            r = lite(request.data)
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

def sendmail(**data) -> dict:
    """Sends email using supplied SMTP settings
    Args:
        data (dict): mail data
    Returns:
        dict: jsonified response
    """    
    msg = Message(
        subject=data['subject'],
        recipients=[data['reciever']],
        html=data['html'],
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
app.register_blueprint(install)    # Remove this line after installation (for extra sec)
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
app.register_blueprint(editor)
# Dashboard

# User
app.register_blueprint(productuser)
app.register_blueprint(bloguser)
app.register_blueprint(mains)
app.register_blueprint(notfound)
app.register_blueprint(extra)
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
app.jinja_env.globals.update(load_blogs=rf.load_blogs)
app.jinja_env.globals.update(load_products=rf.load_products)
app.jinja_env.globals.update(loaddate=loaders.dateformatter)
app.jinja_env.globals.update(link_for=rf.link_for)
app.jinja_env.globals.update(dictcast=rf.ks_todict)
app.jinja_env.globals.update(setattribute=dataparser.Obj)
app.jinja_env.globals.update(htmltext=rf.ks_html2text)
app.jinja_env.globals.update(version=rf.version)


# hooks
# hooks