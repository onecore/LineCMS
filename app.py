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
# Dashboard imports/views

# Public views
from enginepublic.product import productuser
from enginepublic.blog import bloguser
from enginepublic.main import mains
# Public views

ckeditor = CKEditor()

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'svg', 'ico'])
version = "1.4"
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

ckeditor.init_app(app)

UPLOAD_FOLDER = 'static/dashboard/uploads'
UPLOAD_FOLDER_PRODUCTS = 'static/dashboard/uploads/products'
UPLOAD_FOLDER_BLOG = 'static/dashboard/uploads/blog'
app.secret_key = '\xb2\xcb\x06\x85\xb1\xcfZ\x9a\xcf\xb3h\x13\xf6\xa6\xda)\x7f\xdd\xdb\xb2BK>'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

"""
Blueprinted routes
"""
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

app.register_blueprint(productuser)
app.register_blueprint(bloguser)
app.register_blueprint(mains)


# @app.route("/<file>.txt")
# @app.route("/<file>.xml")
# def robot_map_generator(file):
#     pass
#     # match fil: # needs python 3.11
#     #    case 'robots':
#     #         return robotmap.robot()
#     #     case 'robot':
#     #         return robotmap.robot()
#     #     case 'sitemap':
#     #         return robotmap.sitemap()
#     # return which


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

"""
functions for Jinja templating (Public)
"""
app.jinja_env.globals.update(loadblogs=loaders.loadblogs)
app.jinja_env.globals.update(loadproducts=loaders.loadproducts)
