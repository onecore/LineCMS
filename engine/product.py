from flask import Blueprint, render_template, request, redirect, g
import dataengine
from flask_paginate import Pagination, get_page_parameter
import templater as temple

product = Blueprint("product", __name__)


@product.route("/product-new", methods=['POST', 'GET'])
def product_new():
    return render_template("/dashboard/product-new.html")


@product.route("/product-manage", methods=['POST', 'GET'])
def product_mng():
    alert = ""
    de = dataengine.knightclient()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pr = de.get_product_listings()
    tt = len(pr)
    pagination = Pagination(page=page, total=tt,
                            search=search, record_name='product', css_framework="bootstrap5")

    return render_template("/dashboard/product-manage.html", blog=pr, pagination=pagination, alert=alert)
