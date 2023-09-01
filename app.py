# KnightSolutions Canada
# www.KnightSolutions.ca - Client Files / Dashboard
# Aug 31,2023
# MARP - Python 3

import flask
from flask import Flask, render_template, request, jsonify, session
import sqlite3

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')


app.secret_key = '\xb2\xcb\x06\x85\xb1\xcfZ\x9a\xcf\xb3h\x13\xf6\xa6\xda)\x7f\xdd\xdb\xb2BK>'

# session['owner'] = False

# Owner Dashboard


@app.route("/dashboard")
def dash():
    data = None

    return render_template("", data=data)


# Start - Route functions
@app.route("/", methods=['POST', 'GET'])
@app.route("/index", methods=['POST', 'GET'])
def index():
    return render_template("index.html")


@app.route("/inquire", methods=['POST', 'GET'])
def messageRec():
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


@app.route("/messages")
def message():

    con = sqlite3.connect("knightstudiomsg")
    cur = con.cursor()
    ret = cur.execute("SELECT * FROM MESSAGES")
    data = ret.fetchall()
    con.close()

    return render_template("messages.html", data=data)


@app.route("/log")
def login():
    return render_template("log.html")


@app.route("/product/<product_name>")
def product_show(product_name):
    return product_name

# End - Route functions
