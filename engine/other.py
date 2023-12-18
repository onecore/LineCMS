"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
from flask import Blueprint, render_template, redirect, session
import dataengine
from helpers import checkpoint
other = Blueprint("other", __name__)
version = "1.4"

de = dataengine.SandEngine()
log = de.log


@other.route("/logoff")
@checkpoint.onlylogged
def logout():
    try:
        log("Logged out, Session deleted")
        del session['authenticated']
    except Exception as e:
        pass
    return redirect("/")


@other.route("/other")
@checkpoint.onlylogged
def helpv():
    dt = de.load_data_index(None)  # loads datas
    return render_template("dashboard/help.html", version=version, data=dt)


@other.route("/mwebsite")
@checkpoint.onlylogged
def logpage():
    data = de.get_logs()
    return render_template("dashboard/log.html", data=data)