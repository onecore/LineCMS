from flask import Blueprint, render_template, request, redirect, g, send_from_directory, url_for, jsonify
import dataengine
from flask_paginate import Pagination, get_page_parameter
import templater as temple
import json
import os
from icecream import ic
from engine.product import getimages, getmainimage
from decimal import Decimal
import stripe

UPLOAD_FOLDER_PRODUCTS = 'static/dashboard/uploads/products'

loadtheme_ = dataengine.knightclient()
themes = loadtheme_.themeget()[0]

productuser = Blueprint(
                        "productuser", __name__, static_folder='static', static_url_path='/static/SYSTEM/default'
                        )

ps = dataengine.knightclient()
global shipcountries, shiprates, shipstatus
sk, pk, ck, _, wk, wsk,shipstatus,shiprates,shipcountries = ps.productsettings_get() # wk is not needed
stripe.api_key = sk

def price(price) -> int:
    "Stripe friendly price"
    o = round(Decimal(price)*100) # Decimal to keep 2 decimal places from html input, Float doesn't work as it doesn keep the decimals
    return o

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

def parserate(name,amount,mins,maxs):
    clone =  {
                "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {"amount": price(amount), "currency": ck},
                        "display_name": name,
                        "delivery_estimate": {
                            "minimum": {"unit": "business_day", "value": int(mins)},
                            "maximum": {"unit": "business_day", "value": int(maxs)},
                   },
                },
            }
    return clone

def ratetemplater(obj):
    options = []
    parsedobj = None
    try:
        parsedobj = eval(obj)
    except:
        print("Unable to parse ship rates")
        parsedobj = {}
    if parsedobj:
        for rate_name,rate_data in parsedobj.items():
            options.append(parserate(rate_name,rate_data[0],rate_data[1],rate_data[2]))
        return options
    return []

def deductquant(id,variant,quantity):
    pass
    
@productuser.route('/event', methods=['POST'])
def new_event():
    """
    Stripe webhook
    """
    sk, pk, ck, _, wk, wsk,shipstatus,shiprates,shipcountries = ps.productsettings_get() # wk is not needed

    event = None
    payload = request.data
    signature = request.headers['STRIPE_SIGNATURE']
    try:
        event = stripe.Webhook.construct_event(payload, signature, wsk)
    except Exception as e:
        ic(e)
    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(event['data']['object'].id, expand=['line_items'])
        items = []
        for item in session.line_items.data:
            items.append([item.description,item.quantity])
        
        order = {
                "customer_name":session.customer_details.name,
                "customer_email":session.customer_details.email,
                "amount_total":  f'${session.amount_total/100:.02f} {item.currency.upper()}',
                "created":session.created,
                "payment_status": session.payment_status,
                "customer_country": session.customer_details.address.country,
                "customer_postal": session.customer_details.address.postal_code,
                "currency": session.currency,
                "items": str(items),
                "session_id": session.id,
                
                "metadata": session.metadata,
                "address": session.customer_details.address.line1,
                "phone": session.customer_details.phone,
                "shipping_cost": ""
                }
        if shipstatus == "on":
            order["shipping_cost"] = session.shipping_cost.amount_total
        de = dataengine.knightclient()        
        de.productorders_set(order)
    return {'success': True}


def check(data):
    _, _, _, _, _, _,shipstatus,shiprates,shipcountries = ps.productsettings_get() # wk is not needed
    
    _de = dataengine.knightclient()
    items = []
    load_items = []
    product_meta = {}
    for product, values in data.items():
        _, _price, _quantity, _variant = values.split(",")
        def includevariant():
            selected_variant = ""
            if _variant != "Available variants":
                selected_variant = _variant
                return f" - Variant: {selected_variant}"
            return selected_variant
            
        product_data = _de.get_product_single(route=False, checkout=product)
        product_meta[product_data[1] + includevariant()] = product
        clone = {
                'price_data': {
                    'product_data': {
                        'name': product_data[1] + includevariant(),
                    },
                    'unit_amount': price(_price),
                    'currency': ck.lower(),
                },
                'quantity': int(_quantity),
                }

        items.append(clone)

    if shipstatus == "on":  # If shipping Enabled
        
        def parsetolist(shipcountries):
            if "," in shipcountries:
                return shipcountries.split(",")
            if len(shipcountries):
                return [shipcountries]
            return ["US","CA"]
        
        shipratesparsed = ratetemplater(shiprates)    
        shipcountries = parsetolist(shipcountries)
        checkout_session = stripe.checkout.Session.create(
            # Below parameters enable shipping
            shipping_address_collection={"allowed_countries": shipcountries},
            shipping_options=shipratesparsed,
            line_items=items,
            payment_method_types=['card'],
            mode='payment',
            success_url=request.host_url + 'order/success',
            cancel_url=request.host_url + 'order/cancel',
            metadata = product_meta,
        )
    
    else:
        checkout_session = stripe.checkout.Session.create(
            line_items=items,
            payment_method_types=['card'],
            mode='payment',
            success_url=request.host_url + 'order/success',
            cancel_url=request.host_url + 'order/cancel',
            metadata=product_meta
        )
    
    ic(product_meta)
    return checkout_session.url


@productuser.route('/product-checkout', methods=['GET', 'POST'])
def prodcheck():
    if request.method == "POST":
        prdata = {}
        try:
            prdata = eval(request.data)
        except Exception as e:
            return jsonify({"status": 0})

        if prdata:
            clientres = check(prdata)
            return jsonify({'c': clientres})

        return jsonify({"status": 0})
    else:
        return jsonify({"status": 0})


@productuser.route('/product-list', methods=['GET', 'POST'])
def productlist():
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
    products = de.get_product_listings()
    search = False
    q = request.args.get('q')
    if q:
        search = q
    page = request.args.get(get_page_parameter(), type=int, default=1)
    tt = len(products)
    pagination = Pagination(page=page, total=tt,
                            search=search, record_name='products', css_framework="bootstrap")
    return render_template(f"/SYSTEM/{themes}/product-list.html", data=dt, mod=mod, products=products, pagination=pagination)


@productuser.route('/order/success')
def prsuccess():
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
    return render_template(f"/SYSTEM/{themes}/order-success.html",data=dt,mod=mod)


@productuser.route('/order/cancel')
def prcancel():
    return redirect("/product-list")


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
