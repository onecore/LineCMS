"""
SandCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.sandcms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
from flask import Blueprint, render_template, request, redirect, session
import dataengine

logins = Blueprint("logins", __name__)


@logins.route("/login", methods=['GET', 'POST'])
def login():
    """
    authenticator for dashboad route
    """
    if request.method == 'POST':
        _u = request.form.get('uname')
        _p = request.form.get('pwd')
        try:
            _de = dataengine.SandEngine()
            _cred = _de.get_cred(_u, _p)
            _cred_data = _cred[0]
            if _cred_data[0] == _u and _cred_data[1] == _p:
                # Set session
                session['authenticated'] = (_u, _p)
                return redirect("/dashboard")
            else:
                return render_template("dashboard/login.html", error=True)
        except Exception as e:
            return render_template("dashboard/login.html", error=True)
    if 'authenticated' in session:
        if len(session['authenticated']):
            return redirect("/dashboard")
    return render_template("dashboard/login.html", error=False)
