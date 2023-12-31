"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
import json
import settings
import dataengine
from markupsafe import Markup
from helpers import dataparser
from engine.product import getimages
from ast import literal_eval as lite
from flask_paginate import Pagination, get_page_parameter
from engine.product import retrieve_session, product_deduct
from flask import Blueprint, render_template, request, redirect, send_from_directory



de = dataengine.SandEngine()
themes = de.themeget()[0]

productuser = Blueprint(
                        "productuser", __name__, static_folder='static', static_url_path='/static/SYSTEM/'+themes
                        )


class pagination(Pagination):
    """Modified removed numbered links"""
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

def safeget(ret,val):
    try:
        return lite(ret)
    except:
        return val

def variantpush(v, i, js=False) -> dict:
    """
    function to change images into a dictionary with index,
    purpose to show variant image in lightslider when variant changed
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

@productuser.route('/product-list', methods=['GET', 'POST'])
@productuser.route('/products', methods=['GET', 'POST'])
def productlist():
    "views - product list"
    dt = de.load_data_index(None)  # loads datas
    modules_settings = de.load_modules_settings()
    all_d = modules_settings[0]
    mod = {
        "popup": safeget(all_d[0],"0"),
        "announcement": safeget(all_d[1],"0"),
        "uparrow": safeget(all_d[2],"0"),
        "socialshare": safeget(all_d[3],"0"),
        "videoembed": safeget(all_d[4],"0"),
        "custom": safeget(all_d[5],"0"),
        "extras": safeget(all_d[6],"0"),
    }


    alert=None
    par_q = request.args.get('search')
    par_c = request.args.get('category')
    
    if par_c == settings.productlist_select_none: # if the front end's select is modified this should also be modified.
        par_c = ""
        
    showpager = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 15
    offset = (page - 1) * int(per_page)

    if par_q or par_c:
        products = de.get_product_listings(custom={"s":par_q,"c":par_c,"off":offset,"perp":per_page})
    else:
        products = de.get_product_listings(quer=[offset,per_page])

    products_count = de.get_product_listings(getcount=True)[0]
    products_cats = de.get_product_listings(getcats=True)

    if products:
        if per_page > len(products):
            showpager = False
    else:
        showpager = False
        products = []

    paginate = pagination(page=page, total=products_count,record_name='products',css_framework="bootstrap5",
                            inner_window=3,outer_window=3,prev_label="< Previous Page",next_label="Next Page >",alignment="center")
    return render_template(f"/SYSTEM/{themes}/product-list.html", data=dt, mod=mod, products=products, pagination=paginate,showpager=showpager,page=page,
                           categories=products_cats,selectedcat=par_c)


@productuser.route('/order/success')
def purchase_success():
    "views - checkout success (stripe call)"
    try:
        sid = request.args.get("sid")
        session_info = retrieve_session(sid)
        prod_list = session_info['metadata']
        prod_ids = prod_list.values()
        product_deduct(prod_list)
    except:
        prod_ids = []


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
    # process prod_ids thru js (remove from LS)
    return render_template(f"/SYSTEM/{themes}/order-success.html",data=dt,mod=mod,prod_ids=list(prod_ids))


@productuser.route('/order/cancel')
def purchase_cancel():
    "views - checkout cancelled/error (stripe call)"
    return redirect("/product-list")


@productuser.route("/product/<pid>", methods=['GET', 'POST'])
@productuser.route("/product/<new>/<pid>", methods=['GET', 'POST'])
def pproductpage(new=None, pid=None):
    dt = de.load_data_index(None)  # loads datas
    modules_settings = de.load_modules_settings()
    all_d = modules_settings[0]
    product = dataparser.Obj("product",de.get_product_single(pid))
    mod = {
        "popup": lite(all_d[0]),
        "announcement": lite(all_d[1]),
        "uparrow": lite(all_d[2]),
        "socialshare": lite(all_d[3]),
        "videoembed": lite(all_d[4]),
        "custom": lite(all_d[5]),
        "extras": lite(all_d[6]),
    }
    
    if not product:
        return redirect("/product-manage")
    
    variants = lite(product.variants)  
    productinfo = lite(product.variant_details)
    jvariants = json.dumps(variants)
    jproductinfo = json.dumps(productinfo)
    imags = getimages(product.images)
    return render_template(f"/SYSTEM/{themes}/product.html",
                           product=product, 
                           mod=mod, 
                           data=dt,
                           new=new, 
                           images=imags,
                           variants=variants, 
                           productinfo=productinfo,
                           jvariants=jvariants,  # Javascript obj
                           jproductinfo=jproductinfo, # Javascript obj
                           jslides=variantpush(variants, imags, js=True),  # Javascript obj
                           jslidespy=variantpush(variants, imags, js=False), # Python obj
                           similarproducts=de.productsimilar(settings.product_similar_load, product.category),  
                           mainimage=product.mainimage,
                           )


@productuser.route("/ks/<folder>/<file>")
def staticgetter(folder: str, file: str) -> str:
    "jj formatter - returns image file"
    return send_from_directory(f"static/SYSTEM/default/{folder}", file)
