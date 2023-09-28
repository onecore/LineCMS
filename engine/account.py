from flask import Blueprint, render_template, request, redirect, g, session, url_for
import dataengine
from flask_paginate import Pagination, get_page_parameter
import templater as temple

account = Blueprint("account", __name__)

_logger = dataengine.knightclient()
log = _logger.log


@account.route("/account", methods=['POST', 'GET'])
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
            log("Account settings failed error: ", e)
            return False
    try:
        _de = dataengine.knightclient()
        _cred = _de.get_cred(
            session['authenticated'][0], session['authenticated'][1])
        _cred_data = _cred[0]
        return render_template("dashboard/account.html", data=_cred_data, error=error, success=success)
    except Exception as e:
        return redirect("/logoff")
