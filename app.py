# KnightSolutions Canada
# www.KnightSolutions.ca - Client Files / Dashboard
# Aug 31,2023
# MARP - Python 3
import dataengine
import sqlite3
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import flask

version = "1.4"
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
app.secret_key = '\xb2\xcb\x06\x85\xb1\xcfZ\x9a\xcf\xb3h\x13\xf6\xa6\xda)\x7f\xdd\xdb\xb2BK>'

# Owner Dashboard


@app.route("/")
@app.route("/index")
def index():
    """
    main page
    """
    return render_template("main.html")


@app.route("/dashboard", methods=['POST', 'GET'])
def dashboard_main():
    """
    main dashboard page
    """
    de = dataengine.knightclient()
    dt = de.load_data_index(None)  # loads datas
    if 'authenticated' in session:
        if len(session['authenticated']):
            return render_template("dashboard.html", data=dt)
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
                success = True
                de_ = dataengine.knightclient()
                de_.update_credential(session['authenticated'][0], p2)
        except Exception as e:
            print("Exception 'Account_settings change' ", e)
            pass
    try:
        _de = dataengine.knightclient()
        _cred = _de.get_cred(
            session['authenticated'][0], session['authenticated'][1])
        _cred_data = _cred[0]
        return render_template("account.html", data=_cred_data, error=error, success=success)
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
    return render_template("messages.html", data=data)


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
                return render_template("login.html", error=True)
        except Exception as e:
            print("Error: ", e)
            return render_template("login.html", error=True)
    if 'authenticated' in session:
        if len(session['authenticated']):
            return redirect(url_for("dashboard_main"))
    return render_template("login.html", error=False)


@app.route("/product/<product_name>")
def product_show(product_name):
    return product_name

# End - Route functions
