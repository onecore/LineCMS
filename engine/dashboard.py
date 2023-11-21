"""
SandCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.sandcms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
from flask import Blueprint, render_template, request, redirect, session, redirect
import dataengine
from helpers import themeengine,checkpoint
import settings

dashboard = Blueprint("dashboard", __name__)
version = "1.4"
@dashboard.route("/dashboard", methods=['POST', 'GET'])
@checkpoint.onlylogged
def dashboard_main():
    """
    main dashboard page
    """
    error, success = False, False
    de = dataengine.SandEngine()
    dt = de.load_data_index(None)  # loads datas

    tmplist = themeengine.templates_list
    theme = de.themeget()
    if not theme:
        de.themeset("default")
        theme = ("default")


    if request.method == "POST":

        u_sitename = request.form.get('sitename')
        u_description = request.form.get('description')
        u_metadescription = request.form.get('meta_description')
        u_metakeywords = request.form.get('meta_keywords')
        u_footercopyright = request.form.get('footercopyright')
        u_number = request.form.get('sitenumber')
        u_email = request.form.get('siteemail')
        u_address = request.form.get('siteaddress')
        dicts = {
            "sitename": u_sitename,
            "description": u_description,
            "meta_description": u_metadescription,
            "meta_keywords": u_metakeywords,
            "footercopyright": u_footercopyright,
            "sitenumber": u_number,
            "siteemail": u_email,
            "siteaddress": u_address
        }

        for k, v in dicts.items():
            if k not in settings.inputs_dashboard_settings and len(v) <= settings.inputs_dashboard_minumum_length:
                error = f"Some information must be {settings.inputs_dashboard_minumum_length} characters or more"
        if error: 
            return render_template("dashboard/dashboard.html", data=dt, error=error, success=success, tmplist=tmplist, tmpcurrent=theme)
        else:
            upd = dataengine.SandEngine()
            if (upd.update_websitesettings(dicts, owner=session['authenticated'][0])):
                dt = de.load_data_index(None)  # loads datas
                return render_template("dashboard/dashboard.html", data=dt, error=False, success=True, tmplist=tmplist, tmpcurrent=theme)
            else:
                error = "System cannot process your request"
                return render_template("dashboard/dashboard.html", data=dt, error=error, success=False, tmplist=tmplist, tmpcurrent=theme)
            
    return render_template("dashboard/dashboard.html", data=dt, error=error, success=success, tmplist=tmplist, tmpcurrent=theme)


