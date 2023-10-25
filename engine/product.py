from flask import Blueprint, render_template, request, redirect, g
import dataengine
from flask_paginate import Pagination, get_page_parameter
import templater as temple
import json
import os
from icecream import ic
from helpers import currency
from helpers import country

UPLOAD_FOLDER_PRODUCTS = 'static/dashboard/uploads/products'

product = Blueprint("product", __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'svg', 'ico'])


def allowed_file(filename) -> str:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def getimages(ids):
    res = []
    # Iterate directory
    dir_path = f"{UPLOAD_FOLDER_PRODUCTS}/{ids}"
    for file_path in os.listdir(dir_path):
        # check if current file_path is a file
        if os.path.isfile(os.path.join(dir_path, file_path)) and allowed_file(file_path):
            # add filename to list
            res.append(file_path)
    if res:
        return res
    else:
        return []


def getmainimage(ids):
    res = []
    # Iterate directory
    dir_path = f"{UPLOAD_FOLDER_PRODUCTS}/{ids}/mainimage"
    for file_path in os.listdir(dir_path):
        # check if current file_path is a file
        if os.path.isfile(os.path.join(dir_path, file_path)) and allowed_file(file_path):
            # add filename to list
            res.append(file_path)
    if res:
        return res[0]
    else:
        return ""


def variantimagemodifier(d: bytes) -> 'json':
    """
    tuple->list->tuple, checks if file exists, else modify db data to avoid loading file that doesn't exists
    """
    d = list(d)
    _variants = eval(d[3])
    _variants_new = {}
    # mainimage
    for variant_name, image_path in _variants.items():  # variants
        if not os.path.isfile(image_path):
            _variants_new[variant_name] = ""
        else:
            _variants_new[variant_name] = image_path
    d[3] = _variants_new
    d[8] = json.dumps(getimages(d[13]))
    d[9] = getmainimage(d[13])
    de = dataengine.knightclient()
    modifierinsert = de.productimagesmod(
        _variants_new, d[13])
    return tuple(d)


@product.route("/product-settings", methods=['GET', 'POST'])
def product_sett():
    import currencies

    error, success = None, None
    currencieslist = currency.currency
    de = dataengine.knightclient()
    settings = de.productsettings_get()

    if request.method == "POST":
        skey = request.form.get("skey")
        pkey = request.form.get("pkey")
        ckey = request.form.get("ckey")
        wkey = request.form.get("wkey")
        wskey = request.form.get("wskey")
        print(request.form)
        
        if skey and pkey and ckey:
            _set = de.productsettings_set(skey, pkey, ckey,wkey,wskey)
            if _set:
                settings = de.productsettings_get()
                success = 1
        else:
            error = "Some information is missing"
            
            
        # {
        #     "shipping_rate_data": {
        #     "type": "fixed_amount",
        #     "fixed_amount": {"amount": 0, "currency": "usd"},
        #     "display_name": "Free shipping",
        #     "delivery_estimate": {
        #         "minimum": {"unit": "business_day", "value": 5},
        #         "maximum": {"unit": "business_day", "value": 7},
        #     },
        #     },
        # }
    return render_template("/dashboard/product-settings.html", countries = country.countries, currencies=currencieslist, error=error, success=success, settings=settings)


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
    setup = False
    de = dataengine.knightclient()
    _settings = de.productsettings_get()
    if not _settings[0] or not _settings[1] or not _settings[2]:
        setup = True
    return render_template("/dashboard/product-new.html", setup=setup)


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


@product.route("/product-orders", methods=['POST', 'GET'])
def product_orders():
    return render_template("/dashboard/product-orders.html")


