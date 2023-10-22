from flask import Blueprint, render_template, request, redirect, g, send_from_directory
import dataengine
from flask_paginate import Pagination, get_page_parameter
import templater as temple
import json
import os
from icecream import ic
from engine.product import getimages, getmainimage
import stripe

UPLOAD_FOLDER_PRODUCTS = 'static/dashboard/uploads/products'

themes = "default"

productuser = Blueprint(
                        "productuser", __name__, static_folder='static', static_url_path='/static/SYSTEM/default'
                        )

ps = dataengine.knightclient()
sk, pk, ck, _ = ps.productsettings_get()
stripe.api_key = sk


def variantpush(v, i, js=False):
    """
    function to change images into a dictionary with index,
    purpose to show image in lightslider when variant changed, actual variant image will show
    """
    c, d = 0, {}
    for im in i:  # images
        d[im] = c
        c = c + 1
    for key, val in v.items():  # variants
        if v[key]:
            d[val] = c
            c = c + 1
    if js:
        return json.dumps(d)
    return d


@productuser.route('/product-checkout', methods=['GET', 'POST'])
def prodcheck():
    if request.method == "POST":
        print(request.data)

    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'product_data': {
                        'name': "Product 1",
                    },
                    'unit_amount': 200,
                    'currency': 'usd',
                },
                'quantity': 1,
            },
            {
                'price_data': {
                    'product_data': {
                        'name': "Product 2",
                    },
                    'unit_amount': 100,
                    'currency': 'usd',
                },
                'quantity': 1,
            },
        ],
        payment_method_types=['card'],
        mode='payment',
        success_url=request.host_url + 'order/success',
        cancel_url=request.host_url + 'order/cancel',
    )
    return redirect(checkout_session.url)


@productuser.route('/order/success')
def prsuccess():
    return render_template('success.html')


@productuser.route('/order/cancel')
def prcancel():
    return render_template('cancel.html')


@productuser.route("/product/<pid>", methods=['GET', 'POST'])
@productuser.route("/product/<new>/<pid>", methods=['GET', 'POST'])
def publicproductpage(new=None, pid=None):
    de = dataengine.knightclient()
    dt = de.load_data_index(None)  # loads datas
    modules_settings = de.load_modules_settings()
    all_d = modules_settings[0]
    mod = {
        "popup": eval(all_d[0]),
        "announcement": eval(all_d[1]),
        "uparrow": eval(all_d[2]),
        "socialshare": eval(all_d[3]),
        "videoembed": eval(all_d[4]),
        "custom": eval(all_d[5]),
        "extras": eval(all_d[6]),
    }
    product = de.get_product_single(pid)
    variants = eval(product[3])
    productinfo = eval(product[10])
    jvariants = json.dumps(variants)
    jproductinfo = json.dumps(productinfo)
    imags = getimages(product[13])
    return render_template(f"/SYSTEM/{themes}/product.html",
                           product=product, mod=mod, data=dt,
                           new=new, images=imags,
                           variants=variants, productinfo=productinfo,
                           jvariants=jvariants, jproductinfo=jproductinfo,
                           jslides=variantpush(variants, imags, js=True),
                           jslidespy=variantpush(variants, imags, js=False),
                           similarproducts=de.productsimilar(6, product[2]),
                           mainimage=product[9],
                           )


@productuser.route("/ks/<folder>/<file>")
def staticgetter(folder: str, file: str) -> str:
    return send_from_directory(f"static/SYSTEM/default/{folder}", file)
