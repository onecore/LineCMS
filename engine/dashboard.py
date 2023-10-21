from flask import Blueprint, render_template, request, redirect, g, session, jsonify, url_for, redirect
import dataengine
from flask_paginate import Pagination, get_page_parameter
import templater as temple

dashboard = Blueprint("dashboard", __name__)
version = "1.4"


@dashboard.route("/dashboard", methods=['POST', 'GET'])
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
    return redirect("/login")
