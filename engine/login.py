from flask import Blueprint, render_template, request, redirect, g, session, url_for
import dataengine
from flask_paginate import Pagination, get_page_parameter

logins = Blueprint("logins", __name__)

_logger = dataengine.knightclient()
log = _logger.log


@logins.route("/login", methods=['GET', 'POST'])
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
                log("Login success adding to session")
                # Set session
                session['authenticated'] = (_u, _p)
                return redirect("/dashboard")
            else:
                log("Login failed, session deleted")
                return render_template("dashboard/login.html", error=True)
        except Exception as e:
            return render_template("dashboard/login.html", error=True)
    if 'authenticated' in session:
        if len(session['authenticated']):
            return redirect("/dashboard")
    return render_template("dashboard/login.html", error=False)
