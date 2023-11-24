"""
SandCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.sandcms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
from flask import Blueprint, render_template, request, redirect, jsonify
import dataengine
from flask_paginate import Pagination, get_page_parameter,get_page_args
from flask import Markup
import json
import os
from helpers import currency, dataparser
from helpers import country
from decimal import Decimal
from helpers import emailparser,checkpoint
from ast import literal_eval as lite
from jinja2 import Template
import stripe
import settings

product = Blueprint("product", __name__)

UPLOAD_FOLDER_PRODUCTS = 'static/dashboard/uploads/products'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'svg', 'ico'])

ps = dataengine.SandEngine()
sk, pk, ck, _, wk, wsk,shipstatus,shiprates,shipcountries,_,_,_,_,_,_ = ps.productsettings_get() # wk is not needed
stripe.api_key = sk
logging = ps.log

class pagination(Pagination):
    def __init__(self, found=0, **kwargs):
        super().__init__(found, **kwargs)

    @property
    def links(self):
        """Get all the pagination links."""
        if self.total_pages <= 1:
            if self.show_single_page:
                return self._get_single_page_link()

            return ""

        if self.css_framework == "bulma":
            s = [
                self.link_css_fmt.format(
                    self.link_size,
                    self.alignment,
                    self.bulma_style,
                    self.prev_page,
                    self.next_page,
                )
            ]
            for page in self.pages:
                s.append(
                    self.single_page(page) if page else self.gap_marker_fmt
                )
            s.append(self.css_end_fmt)
        else:
            s = [self.link_css_fmt.format(self.link_size, self.alignment)]
            s.append(self.prev_page)
            s.append(self.next_page)
            if self.css_framework == "foundation" and self.alignment:
                s.insert(0, F_ALIGNMENT.format(self.alignment))
                s.append("</div>")

        return Markup("".join(s))

def allowed_file(filename) -> str:
    "returns allowed file extensions"
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getimages(ids) -> list:
    "returns product images from local folder"
    res = []
    # Iterate directory
    dir_path = f"{UPLOAD_FOLDER_PRODUCTS}/{ids}"
    try:
        for file_path in os.listdir(dir_path):
            # check if current file_path is a file
            if os.path.isfile(os.path.join(dir_path, file_path)) and allowed_file(file_path):
                # add filename to list
                res.append(file_path)
    except FileNotFoundError: # no images
        pass
    
    if res:
        return res
    else:
        return []
    
def getmainimage(ids) -> str:
    "returns product's main image"


    res = []
    # Iterate directory
    dir_path = f"{UPLOAD_FOLDER_PRODUCTS}/{ids}/mainimage"
    try:
        for file_path in os.listdir(dir_path):
            # check if current file_path is a file
            if os.path.isfile(os.path.join(dir_path, file_path)) and allowed_file(file_path):
                # add filename to list
                res.append(file_path)
    except FileNotFoundError: # no image
        pass

    if res:
        return res[0]
    else:
        return ""

def variantimagemodifier(d: bytes) -> 'json':
    """
    tuple->list->tuple, checks if file exists, else modify db data to avoid loading file that doesn't exists
    """
    d = list(d)
    _variants = lite(d[3])
    if not _variants:
        _variants = {}
    
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

    modifierinsert = ps.productimagesmod(
        _variants_new, d[13])
    return tuple(d)

def loadorderim(key,obj) -> str:
    """
    Returns image path for a product (if any) else use the ni.jpeg
    """
    img = None
    try:
        robj = lite(obj[14])
    except:
        return "/media/ni.jpeg"
    product_id = robj[key]
    im = ps.get_product_single(0,checkout=product_id)
    if im:
        if im[9]:
            img = f"/media/mainimage/{product_id}/{im[9]}"
        elif im[8]:
            ev = lite(im[8])
            img = f"/media/products/{product_id}/{im[8][0]}"
        else:
            img = "/media/ni.jpeg"
    return img

def parseorders(l,obj) -> dict:
    """
    creates a dict contains quant, and image path
    """
    c = {}
    c[l[0]] = {"quantity":l[1],"image":loadorderim(l[0],obj)}
    return c

@product.route("/product-settings", methods=['GET', 'POST'])
@checkpoint.onlylogged
def product_sett():
    "views - product settings"
    error, success = None, None
    currencieslist = currency.currency
    settings = ps.productsettings_get()

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
            _set = ps.productsettings_set(skey, pkey, ckey,wkey,wskey,shipping_enable,shipping_rates,shipping_countries)
            if _set:
                settings = ps.productsettings_get()
                success = 1
        else:
            error = "Some information is missing"
    return render_template("/dashboard/product-settings.html", countries = country.countries, currencies=currencieslist, error=error, success=success, settings=settings)

@product.route("/product-edit/<route>", methods=['POST', 'GET'])
@checkpoint.onlylogged
def product_edt(route):
    "views - product edit"
    if route == "upload-p-variant" or route == "upload-p-variant":
        return ""
    d = ps.get_product_single(route)
    if not d:
        return redirect("/product-manage")
    return render_template("/dashboard/product-edit.html", d=variantimagemodifier(d))

@product.route("/product-new", methods=['POST', 'GET'])
@checkpoint.onlylogged
def product_new():
    "views - create new product"
    setup = False
    _settings = ps.productsettings_get()
    if not _settings[0] or not _settings[1] or not _settings[2]:
        setup = True
    return render_template("/dashboard/product-new.html", setup=setup)

@product.route("/product-manage", methods=['POST', 'GET'])
@product.route("/product-manage/<alert>", methods=['POST', 'GET'])
@checkpoint.onlylogged
def product_mng(alert=None):
    "views - product manage (lists)"
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    offset = (page - 1) * int(per_page)

    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)

    pcount = ps.get_product_listings(getcount=True)[0]
    pr = ps.get_product_listings(quer=[offset,per_page])

    pagination = Pagination(page=page, total=pcount,
                            search=search, record_name='product', css_framework="bootstrap5",alignment="center")
    if request.method == "POST":
        pass
    return render_template("/dashboard/product-manage.html", product=pr, pagination=pagination, alert=alert)

@product.route("/product-orders", methods=['POST', 'GET'])
@checkpoint.onlylogged
def product_orders():
    "views - product orders (lists)"
    alert=None
    search = False
    q = request.args.get('search')
    per_page = request.args.get('pp')
    status = request.args.get('status')
    showpager = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 15
    offset = (page - 1) * int(per_page)

    if status:  
        if status == "Pending":
            s = "select * from productorders where fulfilled=0 AND (ordernumber like '%{}%' OR customer_name like '%{}%') order by id desc limit {},{}".format(q,q,offset,per_page)                
        if status == "Fulfilled":
            s = "select * from productorders where fulfilled=1 AND (ordernumber like '%{}%' OR customer_name like '%{}%') order by id desc limit {},{}".format(q,q,offset,per_page)
        if status == "Fulfilled Manually":
            s = "select * from productorders where fulfilled=2 AND (ordernumber like '%{}%' OR customer_name like '%{}%') order by id desc limit {},{}".format(q,q,offset,per_page)
    else:
        s = "select * from productorders where fulfilled=0 order by id desc limit {},{}".format(offset,per_page)

    orders = ps.productorders_get(s)
    count_bluf = ps.productorders_get(False,True)[0]

    if orders:
        if per_page > len(orders):
            showpager = False
    else:
        showpager = False
        orders = []
    paging = pagination(page=page, total=count_bluf,
                            search=False, record_name='orders',
                            css_framework="bootstrap5",inner_window=3,outer_window=3,prev_label="< Previous Page",next_label="Next Page >",alignment="center")

    return render_template("/dashboard/product-orders.html", orders=orders, page=page,per_page=per_page,pagination=paging, alert=alert,status=status,showpager=showpager)

@product.route("/product-orders/<ids>", methods=['POST', 'GET'])
@checkpoint.onlylogged
def product_orders_single(ids):
    "views - product order single"
    order = ps.productorders_single_get(ids)
    temp = ps.productsettings_get()
    _comp = ps.load_data_index(0)
    hist = ps.orderhistory_get(order[19])
    template = ""
    alert=None
    shipping_fee = None
    ordersobj = None

    try:
        history = dict(lite(hist[0]).items())
    except Exception as e:
        history = {}
    try:
        temp_status = lite(temp[12])['fulfilled']
        if int(temp_status):
            template = temp[9]            
    except Exception as e:
        pass
    
    parseditems = []
    if order:
        _order = dataparser.zipper("orders",order)
        ordersobj = dataparser.Order("orders",order)
        items = lite(order[10])
        for orders in items:
            parseditems.append(parseorders(orders,order))
        if order[17]:
            shipping_fee = order[17].replace(".","") # needs to update (tho it works)
            shipping_fee = f'${int(shipping_fee)/100:.02f}' 

    _template = Template(template)
    
    rendered = _template.render(emailparser.data("",_order,_comp,"",_order['tracking'],_order['additional'],True,True))
    
    _template_manual = Template(settings.order_template_manual)
    _manual_rend = _template_manual.render(emailparser.data("",_order,_comp,"",_order['tracking'],_order['additional'],parsedate=True))
    return render_template("/dashboard/product-orders-single.html",
                           order=order,alert=alert,items=parseditems,shipping_fee=shipping_fee,
                           template=rendered,history=history,orderdata=ordersobj,manual_t=_manual_rend)


# --> Start of webhook etc.
def price(price) -> int:
    "Stripe friendly price"
    o = round(Decimal(price)*100) # Decimal to keep 2 decimal places from html input, Float doesn't work as it doesn keep the decimals
    return o

def parserate(name,amount,mins,maxs) -> dict:
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

def ratetemplater(obj) -> list:
    "parces rate into a stripe friendly obj"
    options = []
    parsedobj = None
    try:
        parsedobj = lite(obj)
    except:
        parsedobj = {}
    if parsedobj:
        for rate_name,rate_data in parsedobj.items():
            options.append(parserate(rate_name,rate_data[0],rate_data[1],rate_data[2]))
        return options
    return []        


@product.route('/event', methods=['POST'])
def new_event():
    """
    views - stripe webhook (Only captures 'Completed')
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

        addord = ps.productorders_set(order)
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
            temp_settings = ps.productsettings_get()
            comp_data = ps.load_data_index(0)
            
            # send email using Placed template
            try:
                _set = lite(temp_settings[12])['placed']
                if int(_set):
                    order['ordernumber'] = str(addord)
                    emailparser.parse_send(which="placed",ps=temp_settings,order=order,company=comp_data,shipstatus=shipstatus,parsedate=False)
                    history_obj[3] = {"title":"Customer Notified","message":"Email sent to customer with order details","timestamp":order['created']}
                else:
                    history_obj[3] = {"title":"No Notification sent","message":"Disabled in 'Placed template' settings or Mail configuration","timestamp":order['created']}

            except Exception as e:
                history_obj[3] = {"title":"No Notification sent","message":"Disabled in 'Placed template' settings or Mail configuration","timestamp":order['created']}
                pass
            # send email using Placed template
            args = {"obj":history_obj,"ordernumber":addord}
            ps.orderhistory_add(args) # Update history
            return {'success': True}
        else:
            return {'success': False}
    return {'success': True}

def verifyprice():
    pass

def check(data):
    "parses all the data needed to make a friendly objs for stripe api, returns an api url (checkout)"
    _, _, _, _, _, _,shipstatus,shiprates,shipcountries,_,_,_,_,_,_ = ps.productsettings_get() # wk is not needed
    items = []
    load_items = []
    product_meta = {}
    for product, values in data.items():
        _, _price, _quantity, _variant = values.split(",")
        
        def includevariant(nameonly=False):
            "includes variant in product single page view"
            selected_variant = ""
            if _variant != settings.order_novariant_selected:
                selected_variant = _variant
                if nameonly:
                    return selected_variant
                return f" - Variant: {selected_variant}"
            return selected_variant
            
        product_data = ps.get_product_single(route=False, checkout=product)
        product_meta[product] = {"name":product_data[1],"quantity":_quantity,"variant":includevariant(nameonly=True)}

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

    if shipstatus == "on":  # 'on' shipping Enabled
        onerror = settings.order_error_countries
        
        def parsetolist(shipcountries):
            "casts db obj into list"
            try:
                return lite(shipcountries)
            except:
                return onerror
            return onerror
        
        shipratesparsed = ratetemplater(shiprates)    
        shipcountries = parsetolist(shipcountries)
        checkout_session = stripe.checkout.Session.create(
            # Below parameters enable shipping
            shipping_address_collection={"allowed_countries": shipcountries},
            shipping_options=shipratesparsed,
            line_items=items,
            payment_method_types=settings.order_payment_method,
            mode='payment',
            success_url=request.host_url + 'order/success',
            cancel_url=request.host_url + 'order/cancel',
            metadata = product_meta,
        )
    
    else:
        checkout_session = stripe.checkout.Session.create(
            line_items=items,
            payment_method_types=settings.order_payment_method,
            mode='payment',
            success_url=request.host_url + 'order/success',
            cancel_url=request.host_url + 'order/cancel',
            metadata=product_meta
        )
    
    return checkout_session.url


@product.route('/product-checkout', methods=['GET', 'POST'])
def prodcheck():
    "api style for prod. checkout"
    if request.method == "POST":
        prdata = {}
        try:
            prdata = json.loads(request.data)
        except Exception as e:
            return jsonify({"status": 0})
        
        if prdata:
            clientres = check(prdata)
            return jsonify({'c': clientres})
        return jsonify({"status": 0})
    else:
        return jsonify({"status": 0})

