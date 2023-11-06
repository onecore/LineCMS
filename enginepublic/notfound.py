"""
SandCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.sandcms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
from flask import Blueprint, render_template
import dataengine
from ast import literal_eval as lite

notfound = Blueprint("notfound", __name__)

de = dataengine.knightclient()
log = de.log
themes = de.themeget()[0]


@notfound.route("/notfound.html")
def notfoundfn():
    """
    404 Error Page
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
    return render_template(f"/SYSTEM/{themes}/notfound.html", data=dt, mod=mod)
