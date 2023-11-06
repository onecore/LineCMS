"""
SandCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.sandcms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
from flask import Blueprint, render_template
import dataengine
from ast import literal_eval as lite

mains = Blueprint("mains", __name__)

de = dataengine.SandEngine()
log = de.log
themes = de.themeget()[0]

@mains.route("/")
@mains.route("/index")
@mains.route("/main")
def main():
    """
    main page / index
    """
    dt = de.load_data_index(None)  # loads datas
    modules_settings = de.load_modules_settings()
    all_d = modules_settings[0]
    mod = {
        "popup": lite(all_d[0]),
        "announcement": lite(all_d[1]),
        "uparrow": lite(all_d[2]),
        "socialshare": lite(all_d[3]),
        "videoembed": lite(all_d[4]),
        "custom": lite(all_d[5]),
        "extras": lite(all_d[6]),
    }
    return render_template(f"/SYSTEM/{themes}/index.html", data=dt, mod=mod)

@mains.route("/sitemap.txt")
def sitemap():
    "views - generated sitemap file"
    pass

@mains.route("/robots.txt")
def robots():
    "views - generated robots file"
    pass
