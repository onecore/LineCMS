# KnightSolutions Canada
# www.KnightSolutions.ca - Client Files / Dashboard
# Aug 31,2023
# MARP - Python 3
import dataengine
import os
import sqlite3
from flask import Flask, flash, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'svg', 'ico'])
version = "1.4"
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
UPLOAD_FOLDER = 'static/dashboard/uploads'
app.secret_key = '\xb2\xcb\x06\x85\xb1\xcfZ\x9a\xcf\xb3h\x13\xf6\xa6\xda)\x7f\xdd\xdb\xb2BK>'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Owner Dashboard


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
@app.route("/index")
@app.route("/main")
def main():
    """
    main page
    """
    de = dataengine.knightclient()
    dt = de.load_data_index(None)  # loads datas

    return render_template("index.html", data=dt)


@app.route("/inquire", methods=['POST'])
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
        return jsonify({'status': True})
    else:
        return jsonify({'status': False})


@app.route("/media/<file>")
def showuploaded(file):
    return send_from_directory("static/dashboard/uploads", file)


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
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
            except Exception as e:
                print("error ", e)
                # if fails, revert to sample logo
                d_e.update_data_uploads("control", "logo", 'sample.png',
                                        "owner", session['authenticated'][0])
                filename = "sample.png"
            return jsonify({"status": filename})
    return jsonify({"status": "success"})


@app.route("/inquire", methods=['POST', 'GET'])
def messageRec():
    try:
        data = request.json
        json = data

        name = json['name']
        email = json['email']
        subject = json['subject']
        message = json['message']
        phone = json['phone']
        dicts = {
            'name': name,
            'email': email,
            'subject': subject,
            'phone': phone,
            'message': message
        }

        return jsonify({"result": 1})

    except Exception as e:
        return jsonify({"result": 0})


@app.route('/upload_fav', methods=['POST'])
def upload_fav():
    if request.method == 'POST':
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
            except Exception as e:
                print("error ", e)
                # if fails, revert to sample logo
                d_e.update_data_uploads("control", "favicon", 'knight.svg',
                                        "owner", session['authenticated'][0])
                filename = "knight.svg"
            return jsonify({"status": filename})
    return jsonify({"status": "success"})


@app.route("/dashboard", methods=['POST', 'GET'])
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
                            return render_template("dashboard/dashboard.html", data=dt, error=False, success=True)
                        else:
                            error = "System cannot process your request"
                            return render_template("dashboard/dashboard.html", data=dt, error=error, success=False)

            return render_template("dashboard/dashboard.html", data=dt, error=error, success=success)
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
                    success = True
                else:
                    success = False
                    error = "System cannot process your request"

        except Exception as e:
            print("Exception 'Account_settings change' ", e)
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


@app.route("/inquire", methods=['POST', 'GET'])
def messagereceive():
    try:
        data = request.json
        json = data
        name = json['name']
        email = json['email']
        subject = json['subject']
        message = json['message']
        con = sqlite3.connect("knightstudiomsg")
        cur = con.cursor()
        params = "INSERT INTO Messages (Name,Subject,Email,Message) VALUES (?,?,?,?)"
        vals = (name, subject, email, message)
        cur.execute(params, vals)
        con.commit()
        con.close()
        return jsonify({"result": 1})
    except Exception as e:
        print(e)
        return jsonify({"result": 0})


@app.route("/logoff")
def logout():
    try:
        del session['authenticated']
    except Exception as e:
        pass
    return redirect(url_for("index"))


@app.route("/messages")
def message():
    con = sqlite3.connect("knightstudiomsg")
    cur = con.cursor()
    ret = cur.execute("SELECT * FROM MESSAGES")
    data = ret.fetchall()
    con.close()
    return render_template("dashboard/messages.html", data=data)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    authenticator for dashboad route
    """
    if request.method == 'POST':
        _u = request.form.get('uname')
        _p = request.form.get('pwd')
        try:
            _de = dataengine.knightclient()
            _cred = _de.get_cred(_u, _p)
            _cred_data = _cred[0]
            if _cred_data[0] == _u and _cred_data[1] == _p:
                print("Auth success")
                # Set session
                session['authenticated'] = (_u, _p)
                return redirect(url_for("dashboard_main"))
            else:
                print("Auth Failed")
                return render_template("dashboard/login.html", error=True)
        except Exception as e:
            print("Error: ", e)
            return render_template("dashboard/login.html", error=True)
    if 'authenticated' in session:
        if len(session['authenticated']):
            return redirect(url_for("dashboard_main"))
    return render_template("dashboard/login.html", error=False)


@app.route("/product/<product_name>")
def product_show(product_name):
    return product_name

# End - Route functions
