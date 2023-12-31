"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
import dataengine
from ast import literal_eval as lite
from flask import Blueprint, render_template
from helpers import dataparser

notfound = Blueprint("notfound", __name__)

de = dataengine.SandEngine()
log = de.log
themes = de.themeget()[0]


@notfound.route("/notfound")
def notfoundfn():
    """
    404 Error Page
    """
    sitedata = dataparser.Obj("site",de.load_data_index(True))
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
    return render_template(f"/SYSTEM/{themes}/notfound.html", site=sitedata, mod=mod)
