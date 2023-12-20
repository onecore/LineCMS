"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
from flask import Blueprint, render_template, request, redirect, session, redirect
import dataengine
from helpers import themeengine,checkpoint, backup
import settings

install = Blueprint("install", __name__)
de = dataengine.SandEngine()


@install.route("/install", methods=['GET','POST'])
def dashboard_install():
    if de.get_cred():
        return ""
    
    if request.method == "POST":
        error = None
        u_name = request.form.get("uname")
        u_pass = request.form.get("pwd")
        u_pass1 = request.form.get("pwd1")

        if [u_name,u_pass,u_pass1]:
            if u_pass == u_pass1:
                if len(u_pass) >= 12:
                    de.install_cred(u_name,u_pass)
                    session['authenticated'] = (u_name, u_pass)
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
