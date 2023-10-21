from flask import Blueprint, render_template, request, redirect, g, session, url_for
import dataengine
from flask_paginate import Pagination, get_page_parameter
import templater as temple

module = Blueprint("module", __name__)

_logger = dataengine.knightclient()
log = _logger.log


@module.route("/modules")
def modules():
    de = dataengine.knightclient()
    dt = de.load_data_index(None)  # loads datas

    modules_settings = de.load_modules_settings()
    all_d = modules_settings[0]
    dicts = {
        "popup": eval(all_d[0]),
        "announcement": eval(all_d[1]),
        "uparrow": eval(all_d[2]),
        "socialshare": eval(all_d[3]),
        "videoembed": eval(all_d[4]),
        "custom": eval(all_d[5]),
        "extras": eval(all_d[6]),
    }
    return render_template("dashboard/modules.html", data=dt, mod=dicts)
