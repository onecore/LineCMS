"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
import settings
import dataengine
from helpers import dataparser
from ast import literal_eval as lite
from flask_paginate import Pagination, get_page_parameter
from flask import Blueprint, render_template, request, redirect

UPLOAD_FOLDER_PRODUCTS = 'static/dashboard/uploads/products'

de = dataengine.SandEngine()
themes = de.themeget()[0]

bloguser = Blueprint(
                    "bloguser", __name__, static_folder='static', static_url_path='/static/SYSTEM/default'
                    )


@bloguser.route(settings.route_blog, methods=['POST', 'GET'])
@bloguser.route(settings.route_blog+"/", methods=['POST', 'GET'])
@bloguser.route(settings.route_blog+"/<url>", methods=['POST', 'GET'])
@bloguser.route(settings.route_blog+"/<new>/<url>", methods=['POST', 'GET'])
def blog_mainview(new=None, url=None):
    """
    views - blog main view
    """
    if url:
        modules_settings = de.load_modules_settings()
        blog = de.get_blog_single(url)
        catsdata = de.get_blog_cat_lists()
        sitedata = dataparser.Obj("site",de.load_data_index(True))
        blogdata = dataparser.Obj("blog",blog)
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

        return render_template(f"/SYSTEM/{themes}/blog.html", site=sitedata, mod=mod, blog=blogdata, all_categories=catsdata, new=new)
    else:
        return redirect("/notfound")


@bloguser.route(settings.route_blog_list, methods=['GET'])
@bloguser.route("/blogs",methods=['GET'])
def blog_list():
    """
    views - blog posts listings
    """
    dt = de.load_data_index(None)  # loads datas
    modules_settings = de.load_modules_settings()
    sitedata = dataparser.Obj("site",de.load_data_index(True))
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
    blogs = de.get_blog_listings()
    
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=len(blogs),
                            search=search, record_name='blogs', css_framework="bootstrap5", align="center")
    return render_template(f"/SYSTEM/{themes}/blog-list.html", site=sitedata,data=dt, mod=mod, blogs=blogs, pagination=pagination)
