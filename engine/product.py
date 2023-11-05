from flask import Blueprint, render_template, request, redirect, g,jsonify
import dataengine
from flask_paginate import Pagination, get_page_parameter
import json
import os
from icecream import ic
from helpers import currency
from helpers import country
from decimal import Decimal
from helpers import emailparser
from ast import literal_eval as lite
from jinja2 import Template
import stripe

product = Blueprint("product", __name__)


ps = dataengine.knightclient()
sk, pk, ck, _, wk, wsk,shipstatus,shiprates,shipcountries,_,_,_,_,_,_ = ps.productsettings_get() # wk is not needed
stripe.api_key = sk
logging = ps.log

UPLOAD_FOLDER_PRODUCTS = 'static/dashboard/uploads/products'
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

def loadorderim(key,obj) -> str:
    """
    Returns image path for a product (if any) else use the ni.jpeg
    """
    img = None
    try:
        robj = eval(obj[14])
    except:
        return "/media/ni.jpeg"
    product_id = robj[key]
    de = dataengine.knightclient()
    im = de.get_product_single(0,checkout=product_id)
    if im:
        if im[9]:
            img = f"/media/mainimage/{product_id}/{im[9]}"
        elif im[8]:
            ev = eval(im[8])
            img = f"/media/products/{product_id}/{im[8][0]}"
        else:
            img = "/media/ni.jpeg"
    return img

def parseorders(l,obj) -> dict:
    """
    Creates a Dict contains quant, and image path
    """
    c = {}
    c[l[0]] = {"quantity":l[1],"image":loadorderim(l[0],obj)}
    return c

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

        shipping_enable = request.form.get("shipping")
        shipping_rates = request.form.get("shippingobj")    
        shipping_countries = request.form.get("cactivated")    
        
        if skey and pkey and ckey:
            _set = de.productsettings_set(skey, pkey, ckey,wkey,wskey,shipping_enable,shipping_rates,shipping_countries)
            if _set:
                settings = de.productsettings_get()
                success = 1
        else:
            error = "Some information is missing"
    ic(settings)
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
    _de = dataengine.knightclient()
    orders = _de.productorders_get()
    alert=None
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    tt = len(orders)
    pagination = Pagination(page=page, total=tt,
                            search=search, record_name='orders', css_framework="bootstrap5")
    return render_template("/dashboard/product-orders.html", orders=orders, pagination=pagination, alert=alert)

@product.route("/product-orders/<ids>", methods=['POST', 'GET'])
def product_orders_single(ids):
    _de = dataengine.knightclient()
    order = _de.productorders_single_get(ids)
    temp = _de.productsettings_get()
    hist = _de.orderhistory_get(order[19])
    template = None
    try:
        history = dict(lite(hist[0]).items())
    except Exception as e:
        history = None
        
    try:
        temp_status = lite(temp[12])['fulfilled']
        if temp_status:
            template = temp[9]
                
    except Exception as e:
        pass
    
    alert=None
    parseditems = []
    shipping_fee = None
    if order:
        items = eval(order[10])
        for orders in items:
            parseditems.append(parseorders(orders,order))
        
        if order[17]:
            shipping_fee = order[17].replace(".","") # needs to update (tho it works)
            shipping_fee = f'${int(shipping_fee)/100:.02f}' 
    print(history)
    return render_template("/dashboard/product-orders-single.html",
                           order=order,alert=alert,items=parseditems,shipping_fee=shipping_fee,
                           template=template,history=history)

def price(price) -> int:
    "Stripe friendly price"
    o = round(Decimal(price)*100) # Decimal to keep 2 decimal places from html input, Float doesn't work as it doesn keep the decimals
    return o

def parserate(name,amount,mins,maxs):
    "Parse shipping rate opt. obj for stripe "
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

@product.route('/event', methods=['POST'])
def new_event():
    """
    Stripe webhook
    """
    sk, pk, ck, _, wk, wsk,shipstatus,shiprates,shipcountries,_,_,_,_,_,_ = ps.productsettings_get() # wk is not needed

    event = None
    payload = request.data
    signature = request.headers['STRIPE_SIGNATURE']
    
    try:
        event = stripe.Webhook.construct_event(payload, signature, wsk)
    except Exception as e:
        logging(f"Stripe Webhook Err -> {e}")
        
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
        
        history_obj = {1: {"title":"Order Placed","message":"","timestamp":order['created']}}
        
        if shipstatus == "on":
            shipstatus = True
            order["shipping_cost"] = session.shipping_cost.amount_total
        else:
            shipstatus = False

        de = dataengine.knightclient()    
        addord = de.productorders_set(order)
        if addord:        
            if order['shipping_cost']:
                ship_fee_ = f"${int(order['shipping_cost'])/100:.02f}"
                history_obj[1]["message"] = f"Order #{addord} - Paid {ship_fee_} for Shipping"
            else:
                history_obj[1]['message'] = f"Order #{addord}"
            
            if order['payment_status'] == "paid":
                history_obj[2] = {"title":"Payment accepted","message":f"Order #{addord} - Paid the amount of {order['amount_total']}","timestamp":order['created']}
            else:
                history_obj[2] = {"title":"Payment unverified","message":f"Order #{addord} - Paid the amount of {order['amount_total']}","timestamp":order['created']}
                

            logging(f"New order placed from: {order['customer_name']} - {order['customer_email']}")
            temp_settings = de.productsettings_get()
            comp_data = de.load_data_index(0)
            
            # { Send email using Placed template
            sendmailer = False
            try:
                _set = lite(temp_settings[12])['placed']
                if int(_set):
                    order['ordernumber'] = str(addord)
                    emailparser.parse_send(which="placed",ps=temp_settings,order=order,company=comp_data,shipstatus=shipstatus)
                    history_obj[3] = {"title":"Customer Notified","message":"Email sent to customer with order details","timestamp":order['created']}
            except Exception as e:
                history_obj[3] = {"title":"No Notification sent","message":"Disabled in 'Placed template' settings or Mail configuration","timestamp":order['created']}
                pass
            # }Send email using Placed template
            args = {"obj":history_obj,"ordernumber":addord}
            de.orderhistory_add(args)
            return {'success': True}
        else:
            return {'success': False}
    return {'success': True}

def check(data):
    _, _, _, _, _, _,shipstatus,shiprates,shipcountries,_,_,_,_,_,_ = ps.productsettings_get() # wk is not needed
    _de = dataengine.knightclient()
    items = []
    load_items = []
    product_meta = {}
    
    for product, values in data.items():
        _, _price, _quantity, _variant = values.split(",")
        
        def includevariant():
            "Dangy..."
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
            try:
                return eval(shipcountries)
            except:
                ["US","CA"]
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
    
    return checkout_session.url


@product.route('/product-checkout', methods=['GET', 'POST'])
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
