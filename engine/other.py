from flask import Blueprint, render_template, request, redirect, g, session, url_for, jsonify
import dataengine
from flask_paginate import Pagination, get_page_parameter

other = Blueprint("other", __name__)
version = "1.4"

de = dataengine.knightclient()
log = de.log


@other.route("/logoff")
def logout():
    try:
        log("Logged out, Session deleted")
        del session['authenticated']
    except Exception as e:
        pass
    return redirect("/")


@other.route("/other")
def helpv():
    dt = de.load_data_index(None)  # loads datas
    return render_template("dashboard/help.html", version=version, data=dt)


@other.route("/mwebsite")
def logpage():
    data = de.get_logs()
    return render_template("dashboard/log.html", data=data)
