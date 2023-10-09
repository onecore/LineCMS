from flask import Blueprint, render_template, request, redirect, g
import dataengine
from flask_paginate import Pagination, get_page_parameter
import templater as temple
import json
import os
UPLOAD_FOLDER_PRODUCTS = 'static/dashboard/uploads/products'

product = Blueprint("product", __name__)


def variantimagemodifier(d: bytes) -> 'json':
    """
    tuple->list->tuple, checks if file exists, else modify db data to avoid loading file that doesn't exists
    """
    d = list(d)
    _variants = eval(d[3])
    _variants_new = {}
    _images = eval(d[8])
    _images_new = []

    # mainimage
    if not os.path.isfile(f"{UPLOAD_FOLDER_PRODUCTS}/{d[13]}/{d[9]}"):
        d[9] = ""

    for variant_name, image_path in _variants.items():  # variants
        if not os.path.isfile(image_path):
            _variants_new[variant_name] = ""
        else:
            _variants_new[variant_name] = image_path

    for imgs in _images:
        if not os.path.isfile(f"{UPLOAD_FOLDER_PRODUCTS}/{d[13]}/{imgs}"):
            pass
        else:
            _images_new.append(imgs)

    d[3] = _variants_new
    d[8] = json.dumps(_images_new)

    de = dataengine.knightclient()
    modifierinsert = de.productimagesmod(
        _variants_new, _images_new, d[9], d[13])
    return tuple(d)


@product.route("/product-edit/<route>", methods=['POST', 'GET'])
def product_edt(route):
    if route == "upload-p-variant" or route == "upload-p-variant":
        return ""
    de = dataengine.knightclient()
    d = de.get_product_single(route)
    if not d:
        return redirect("/product-manage")

    return render_template("/dashboard/product-edit.html", d=variantimagemodifier(d))


@product.route("/product-new", methods=['POST', 'GET'])
def product_new():
    return render_template("/dashboard/product-new.html")


@product.route("/product-manage", methods=['POST', 'GET'])
@product.route("/product-manage/<alert>", methods=['POST', 'GET'])
def product_mng(alert=None):
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

    return render_template("/dashboard/product-manage.html", product=pr, pagination=pagination, alert=alert)
