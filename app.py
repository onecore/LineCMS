# KnightSolutions Canada
# Extendable Content Manage System for any Website template
# www.KnightSolutions.ca - KnightStudio Dashboard / Client files
# Aug 31,2023
# www.sinsoro.com - SinsoroCMS / Client files
# Sept 19, 2023
# Developed by Mark Anthony Pequeras - Python 3.x.x
# Database: Sqlite3

import dataengine
import os
from flask import Flask, Blueprint, g, flash, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flask_ckeditor import CKEditor
from flask_paginate import Pagination, get_page_parameter
import templater as temple
import renderfunc as rf

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

# Owner Dashboard

_logger = dataengine.knightclient()
log = _logger.log


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/product-new", methods=['POST', 'GET'])
def product_new():
    return render_template("/dashboard/product-new.html")


@app.route("/product-manage", methods=['POST', 'GET'])
def product_mng():
    return render_template("/dashboard/product-manage.html")


@app.route("/blog-edit/<url>", methods=['POST', 'GET'])
def blog_edit(url):
    de = dataengine.knightclient()
    blog = de.get_blog_single(url)

    if request.method == 'POST':
        data_body = request.form.get('ckeditor')  # <--
        data_title = request.form.get('title')  # <--
        data_categ = request.form.get('cat')  # <--
        data_imgname = request.form.get('bimg')  # <--
        data_hidden = request.form.get('ishidden')  # <--
        if not data_title:
            return render_template("/dashboard/blog-edit.html", blog=blog, error="Blog title can't be empty")
        if not data_body:
            return render_template("/dashboard/blog-edit.html", blog=blog, error="Blog content can't be empty")
        else:
            data = {"title": data_title, "body": data_body,
                    "category": data_categ, "hidden": data_hidden, "route": blog[6]}
            if data_imgname:
                data["image"] = data_imgname
            else:
                data['image'] = "no-image.jpeg"
            if data_categ:
                data['category'] = data_categ
            else:
                data['category'] = 'blog'
            try:
                if (de.blog_update(data)):
                    return redirect(temple.route_blog+"/1/"+data['route'])
                else:
                    return render_template("/dashboard/blog-edit.html", blog=blog, error="Blog post failed to publish.")
            except Exception as e:
                print(e)
                return render_template("/dashboard/blog-edit.html", blog=blog, error="Blog post failed to publish.")
    return render_template("/dashboard/blog-edit.html", blog=blog)


@app.route("/blog-manage", methods=['POST', 'GET'])
@app.route("/blog-manage/<alert>", methods=['POST', 'GET'])
def blog_manage(alert=None):
    de = dataengine.knightclient()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    blog = de.get_blog_listings()
    tt = len(blog)
    pagination = Pagination(page=page, total=tt,
                            search=search, record_name='blog', css_framework="bootstrap5")

    return render_template("/dashboard/blog-manage.html", blog=blog, pagination=pagination, alert=alert)


@app.route(temple.route_blog_list, methods=['GET'])
def blog_list():
    de = dataengine.knightclient()
    dt = de.load_data_index(None)  # loads datas
    modules_settings = de.load_modules_settings()
    all_d = modules_settings[0]
    mod = {
        "popup": eval(all_d[0]),
        "announcement": eval(all_d[1]),
        "uparrow": eval(all_d[2]),
        "socialshare": eval(all_d[3]),
        "videoembed": eval(all_d[4]),
        "custom": eval(all_d[5]),
        "extras": eval(all_d[6]),
    }
    blogs = de.get_blog_listings()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    tt = len(blogs)
    pagination = Pagination(page=page, total=tt,
                            search=search, record_name='blogs', css_framework="bootstrap5")
    return render_template(temple.render_blog_list, data=dt, mod=mod, blogs=blogs)


@app.route(temple.route_blog, methods=['POST', 'GET'])
@app.route(temple.route_blog+"/", methods=['POST', 'GET'])
@app.route(temple.route_blog+"/<url>", methods=['POST', 'GET'])
@app.route(temple.route_blog+"/<new>/<url>", methods=['POST', 'GET'])
def blog_mainview(new=None, url=None):
    if url:
        de = dataengine.knightclient()
        dt = de.load_data_index(None)  # loads datas
        modules_settings = de.load_modules_settings()
        all_d = modules_settings[0]
        mod = {
            "popup": eval(all_d[0]),
            "announcement": eval(all_d[1]),
            "uparrow": eval(all_d[2]),
            "socialshare": eval(all_d[3]),
            "videoembed": eval(all_d[4]),
            "custom": eval(all_d[5]),
            "extras": eval(all_d[6]),
        }
        blog = de.get_blog_single(url)
        cats = blog[7].split(",")
        cats_list = de.get_blog_cat_lists()
        return render_template(temple.render_blog_single, data=dt, mod=mod, blog=blog, cats=cats, catslist=cats_list, new=new)
    else:
        return redirect(temple.route_blog_list)


@app.route("/blog-new", methods=['POST', 'GET'])
def blog_new():
    if request.method == 'POST':
        data_body = request.form.get('ckeditor')  # <--
        data_title = request.form.get('title')  # <--
        data_categ = request.form.get('cat')  # <--
        data_imgname = request.form.get('bimg')  # <--
        if not data_title:
            return render_template("/dashboard/blog-new.html", error="Blog title required")
        if not data_body:
            return render_template("/dashboard/blog-new.html", error="Blog content required")
        else:
            data = {"title": data_title,
                    "body": data_body, "category": data_categ}
            if data_imgname:
                data["image"] = data_imgname
            else:
                data['image'] = "no-image.jpeg"
            if data_categ:
                data['category'] = data_categ
            else:
                data['category'] = 'blog'
            de = dataengine.knightclient()
            try:
                if (de.blog_publish(data)):
                    return redirect(temple.route_blog+"/1/"+g.new_blog_url)
                else:
                    return render_template("/dashboard/blog-new.html", error="Blog post failed to publish.")
            except Exception as e:
                print(e)
                return render_template("/dashboard/blog-new.html", error="Blog post failed to publish.")
    return render_template("/dashboard/blog-new.html")


@ app.route("/")
@ app.route("/index")
@ app.route("/main")
def main():
    """
    main page
    """
    de = dataengine.knightclient()
    dt = de.load_data_index(None)  # loads datas
    modules_settings = de.load_modules_settings()
    all_d = modules_settings[0]
    mod = {
        "popup": eval(all_d[0]),
        "announcement": eval(all_d[1]),
        "uparrow": eval(all_d[2]),
        "socialshare": eval(all_d[3]),
        "videoembed": eval(all_d[4]),
        "custom": eval(all_d[5]),
        "extras": eval(all_d[6]),
    }
    return render_template("index.html", data=dt, mod=mod)


@ app.route("/module_update", methods=['POST', 'GET'])
def modupdate():
    if request.method == "POST":
        if 'authenticated' in session:  # Logged in
            de = dataengine.knightclient()
            print(">>>>>> ", request.data)
            if (de.update_module(request.data)):
                return jsonify({'status': True})
            else:
                return jsonify({'status': False})
        return "KnightStudio Dashboard build ", version
    else:
        return "KnightStudio Dashboard build ", version


@ app.route("/knightclientapi", methods=['POST', 'GET'])
def knightapi():
    if request.method == "POST":
        if 'authenticated' in session:  # Logged in
            d = dataengine.knightclient()
            if (d.knightclientapi(eval(request.data)['action'])):
                log("API Call success")
                return jsonify({'status': True})
            else:
                log("API Call failed")
                return jsonify({'status': False})
        return "KnightStudio Dashboard build ", version
    else:
        return "KnightStudio Dashboard build ", version


@app.route("/deleapi", methods=['POST', 'GET'])
def delete_api():
    if request.method == "POST":
        if 'authenticated' in session:  # Logged in
            table = request.json['table']
            column = request.json['column']
            value = request.json['value']
            de = dataengine.knightclient()
            if (de.delete_api(table, column, value)):
                return jsonify({"status": 1, "message": "Blog post has been deleted"})
            else:
                return jsonify({"status": 1, "message": "Blog post cannot delete right now"})
    else:
        return jsonify({"status": 0})


@ app.route("/knightclientapiv2", methods=['POST', 'GET'])
def knightapi2():
    if request.method == "POST":
        if 'authenticated' in session:  # Logged in
            d = dataengine.knightclient()
            if (d.knightclientapiv2(eval(request.data))):
                print(request.data)
                log("API Call success")
                return jsonify({'status': True})
            else:
                log("API Call failed")
                return jsonify({'status': False})
        return "KnightStudio Dashboard build ", version
    else:
        return "KnightStudio Dashboard build ", version


@ app.route("/modules")
def modules():
    de = dataengine.knightclient()
    dt = de.load_data_index(None)  # loads datas

    modules_settings = de.load_modules_settings()
    all_d = modules_settings[0]
    dicts = {
        "popup": eval(all_d[0]),
        "announcement": eval(all_d[1]),
        "uparrow": eval(all_d[2]),
        "socialshare": eval(all_d[3]),
        "videoembed": eval(all_d[4]),
        "custom": eval(all_d[5]),
        "extras": eval(all_d[6]),
    }
    log("KSEngine Modules Loaded")
    # print(dicts['popup']['enabled'])
    return render_template("dashboard/modules.html", data=dt, mod=dicts)


@ app.route("/delete/<table>/<id>")
def delete(table, id):
    mid = id
    if 'authenticated' in session:
        d = dataengine.knightclient()
        if d.delete(table, id):
            return jsonify({"status": True})
        else:
            return jsonify("status", False)
    return jsonify({"status": False})


@ app.route("/inquire", methods=['POST'])
def messagerec():
    data = request.json
    json = data
    dicts = {
        'name': json['name'],
        'email': json['email'],
        'phone': json['phone'],
        'message': json['message'],
    }

    _de = dataengine.knightclient()

    if (_de.message(dicts)):
        log("New message from received")
        return jsonify({'status': True})
    else:
        log("New message failed to process")
        return jsonify({'status': False})


@ app.route("/media/<file>")
def showuploaded(file):
    return send_from_directory("static/dashboard/uploads", file)


@ app.route("/media/blog/<file>")
def showuploaded_blog(file):
    return send_from_directory("static/dashboard/uploads/blog", file)


@ app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        log("New Logo upload started")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            print("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("success processing now")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            d_e = dataengine.knightclient()
            try:
                d_e.update_data_uploads("control", "logo", filename,
                                        "owner", session['authenticated'][0])
                log("Logo file uploaded")
            except Exception as e:
                log("Logo upload failed, revert")
                # if fails, revert to sample logo
                d_e.update_data_uploads("control", "logo", 'sample.png',
                                        "owner", session['authenticated'][0])
                filename = "sample.png"
            return jsonify({"status": filename})
    return jsonify({"status": "success"})


@ app.route('/upload-blog', methods=['POST'])
def upload_file_blog():
    print("Blog thumbnail upload")
    if request.method == 'POST':
        log("New Logo upload started")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            print("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("success processing now")
            filename = secure_filename(file.filename)

            file.save(os.path.join(UPLOAD_FOLDER_BLOG, filename))
            d_e = dataengine.knightclient()
            try:
                # d_e.update_data_uploads("control", "logo", filename,
                #                         "owner", session['authenticated'][0])
                log("Post thumbnail uploaded")
            except Exception as e:
                log("Post thumbnail failed, revert")
                # if fails, revert to sample logo
                # d_e.update_data_uploads("control", "logo", 'sample.png',
                #                         "owner", session['authenticated'][0])
                # filename = "sample.png"
            return jsonify({"status": filename})
    return jsonify({"status": "success"})


@ app.route('/upload_fav', methods=['POST'])
def upload_fav():
    if request.method == 'POST':
        log("New Favicon file upload started")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            print("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("success processing now")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            d_e = dataengine.knightclient()
            try:
                d_e.update_data_uploads("control", "favicon", filename,
                                        "owner", session['authenticated'][0])
                log("Favicon file uploaded")
            except Exception as e:
                log("Favicon file failed to upload: ", e)
                # if fails, revert to sample logo
                d_e.update_data_uploads("control", "favicon", 'knight.svg',
                                        "owner", session['authenticated'][0])
                filename = "knight.svg"
            return jsonify({"status": filename})
    return jsonify({"status": "success"})


@ app.route("/dashboard", methods=['POST', 'GET'])
def dashboard_main():
    """
    main dashboard page
    """
    error, success = False, False
    de = dataengine.knightclient()
    dt = de.load_data_index(None)  # loads datas

    if 'authenticated' in session:
        if len(session['authenticated']):
            if request.method == "POST":

                u_sitename = request.form.get('sitename')
                u_description = request.form.get('description')
                u_metadescription = request.form.get('meta_description')
                u_metakeywords = request.form.get('meta_keywords')
                u_footercopyright = request.form.get('footercopyright')
                dicts = {
                    "sitename": u_sitename,
                    "description": u_description,
                    "meta_description": u_metadescription,
                    "meta_keywords": u_metakeywords,
                    "footercopyright": u_footercopyright
                }
                for k, v in dicts.items():
                    if len(v) < 5:
                        error = "Some information must be 5 characters or more"
                        return render_template("dashboard.html", data=dt, error=error, success=success)
                    else:
                        upd = dataengine.knightclient()
                        if (upd.update_websitesettings(dicts, owner=session['authenticated'][0])):
                            dt = de.load_data_index(None)  # loads datas
                            log("Website Information Updated")
                            return render_template("dashboard/dashboard.html", data=dt, error=False, success=True)
                        else:
                            error = "System cannot process your request"
                            log(error, " dashboard POST call")
                            return render_template("dashboard/dashboard.html", data=dt, error=error, success=False)
            return render_template("dashboard/dashboard.html", data=dt, error=error, success=success)
    log("Authenticate failed, returning to login")
    return redirect(url_for("login"))


@app.route("/account", methods=['POST', 'GET'])
def dashboard_account():
    """
    dashboard account settings page
    """
    error = False
    success = False
    if request.method == 'POST':
        try:
            p1 = request.form.get('pwd1')
            p2 = request.form.get('pwd2')
            if p1 != p2:
                error = "Password does not match"
                print("Error 1")

            elif len(p1) < 4 or len(p2) < 4:
                error = "Password must have 5 characters and above"
                print("Error 2")
            else:
                de_ = dataengine.knightclient()
                if de_.update_credential(session['authenticated'][0], p2):
                    log("Account update success")
                    success = True
                else:
                    log("Account update failed")
                    success = False
                    error = "System cannot process your request"

        except Exception as e:
            print("Exception 'Account_settings change' ", e)
            log("Account settings filed error: ", e)
            pass
    try:
        _de = dataengine.knightclient()
        _cred = _de.get_cred(
            session['authenticated'][0], session['authenticated'][1])
        _cred_data = _cred[0]
        return render_template("dashboard/account.html", data=_cred_data, error=error, success=success)
    except Exception as e:
        return redirect(url_for("logout"))


# Start - Route functions


@app.route("/logoff")
def logout():
    try:
        log("Logged out, Session deleted")
        del session['authenticated']
    except Exception as e:
        pass
    return redirect(url_for("main"))


@app.route("/other")
def help():
    de = dataengine.knightclient()
    dt = de.load_data_index(None)  # loads datas
    return render_template("dashboard/help.html", version=version, data=dt)


@app.route("/messages")
def messages():
    # con = sqlite3.connect("knightstudiomsg")
    # cur = con.cursor()
    # ret = cur.execute("SELECT * FROM MESSAGES")
    # data = ret.fetchall()
    # con.close()
    _m = dataengine.knightclient()
    data = _m.get_messages()
    return render_template("dashboard/messages.html", data=data)


@app.route("/mwebsite")
def logpage():
    _l = dataengine.knightclient()
    data = _l.get_logs()
    return render_template("dashboard/log.html", data=data)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    authenticator for dashboad route
    """
    if request.method == 'POST':
        log("New login activity")
        _u = request.form.get('uname')
        _p = request.form.get('pwd')
        try:
            _de = dataengine.knightclient()
            _cred = _de.get_cred(_u, _p)
            _cred_data = _cred[0]
            if _cred_data[0] == _u and _cred_data[1] == _p:
                log("Login success adding to session")
                # Set session
                session['authenticated'] = (_u, _p)
                return redirect(url_for("dashboard_main"))
            else:
                log("Login failed, session deleted")
                return render_template("dashboard/login.html", error=True)
        except Exception as e:
            print("Error: ", e)
            return render_template("dashboard/login.html", error=True)
    if 'authenticated' in session:
        if len(session['authenticated']):
            return redirect(url_for("dashboard_main"))
    else:
        return render_template("dashboard/login.html", error=False)


#~~~~~~~~~~~~ Templating Funcs Start ~~~~~~~~~~~~~#
app.jinja_env.globals.update(blog_list_badge_category=rf.ks_badge_insert)
app.jinja_env.globals.update(admin_button=rf.ks_include_adminbutton)
#~~~~~~~~~~~~ Templating Funcs End ~~~~~~~~~~~~~#
