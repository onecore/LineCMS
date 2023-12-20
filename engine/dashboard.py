"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
from flask import Blueprint, render_template, request, redirect, session, redirect
import dataengine
from helpers import themeengine,checkpoint, backup
import settings, validators

dashboard = Blueprint("dashboard", __name__)
de = dataengine.SandEngine()


@dashboard.route("/install", methods=['GET','POST'])
def dashboard_install():
    if request.method == "POST":
        error = None
        u_email = request.form.get("email")
        u_name = request.form.get("uname")
        u_pass = request.form.get("pwd")
        u_pass1 = request.form.get("pwd1")

        if [u_name,u_pass,u_pass1]:
            if u_pass == u_pass1:
                if len(u_pass) >= 12:
                    de.install_cred(u_name,u_pass)
                    return redirect("/dashboard")
                else:
                    error = "Password must have atleast 10 characters" 
                    return render_template("dashboard/install/install.html",error=error)             
            
            error = "Password doesn't match" 
            return render_template("dashboard/install/install.html",error=error)
        
        else:
            error = "Missing information"
            return render_template("dashboard/install/install.html",error=error)


    return render_template("dashboard/install/install.html")

@dashboard.route("/dashboard", methods=['POST', 'GET'])
@checkpoint.onlylogged
def dashboard_main():
    """
    main dashboard page
    """
    error, success = False, False
    dt = de.load_data_index(None)  # loads datas
    tmplist = themeengine.get_templates()
    # tmplist = themeengine.templates_list
    theme = de.themeget()
    backups = backup.show_backs_list()
    backs_db, backs_rs = backups['db'], backups['rs']
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
            return render_template("dashboard/dashboard.html", data=dt, error=error, success=success, tmplist=tmplist, tmpcurrent=theme,backs_rs=backs_rs,backs_db=backs_db)
        else:
            upd = dataengine.SandEngine()
            if (upd.update_websitesettings(dicts, owner=session['authenticated'][0])):
                dt = de.load_data_index(None)  # loads datas
                return render_template("dashboard/dashboard.html", data=dt, error=False, success=True, tmplist=tmplist, tmpcurrent=theme,backs_rs=backs_rs,backs_db=backs_db)
            else:
                error = "System cannot process your request"
                return render_template("dashboard/dashboard.html", data=dt, error=error, success=False, tmplist=tmplist, tmpcurrent=theme,backs_rs=backs_rs,backs_db=backs_db)
            
    return render_template("dashboard/dashboard.html", data=dt, error=error, success=success, tmplist=tmplist, tmpcurrent=theme,backs_rs=backs_rs,backs_db=backs_db)


