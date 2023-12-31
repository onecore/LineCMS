"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
from flask import Blueprint, render_template, request, redirect, session
import dataengine
from helpers import checkpoint
account = Blueprint("account", __name__)

@account.route("/account", methods=['POST', 'GET'])
@checkpoint.onlylogged
def dashboard_account():
    """
    dashboard account settings page
    """
    error, success = False, False
    if request.method == 'POST':
        try:
            p1 = request.form.get('pwd1')
            p2 = request.form.get('pwd2')
            if p1 != p2:
                error = "Password does not match"
            elif len(p1) < 4 or len(p2) < 4:
                error = "Password must have 5 characters or greater"
            else:
                de_ = dataengine.SandEngine()
                if de_.update_credential(session['authenticated'][0], p2):
                    success = True
                else:
                    success = False
                    error = "System cannot process your request"
        except Exception as e:
            return False
    try:
        _de = dataengine.SandEngine()
        _cred = _de.get_cred(
            session['authenticated'][0], session['authenticated'][1])
        _cred_data = _cred[0]
        print (_cred_data)
        if (_cred_data):
            return render_template("dashboard/account.html", data=_cred_data, error=error, success=success)
        return redirect("/logoff")

    except Exception as e:
        print(e)
        return redirect("/logoff")

