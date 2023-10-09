from flask import Blueprint, render_template, request, redirect, g, send_from_directory
import dataengine
from flask_paginate import Pagination, get_page_parameter
import templater as temple
import json
import os
UPLOAD_FOLDER_PRODUCTS = 'static/dashboard/uploads/products'

themes = "default"

productuser = Blueprint(
                        "productuser", __name__, static_folder='static', static_url_path='/static/SYSTEM/default'
                        )


@productuser.route("/ks/<folder>/<file>")
def staticgetter(folder: str, file: str) -> str:
    return send_from_directory(f"static/SYSTEM/default/{folder}", file)


@productuser.route("/product", methods=['GET', 'POST'])
def publicproductpage(pid=None):
    return render_template(f"/SYSTEM/{themes}/index.html")
