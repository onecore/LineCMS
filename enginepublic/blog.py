from flask import Blueprint, render_template, request, redirect, g, send_from_directory
import dataengine
from flask_paginate import Pagination, get_page_parameter
import templater as temple
import json
import os
import dataengine
from flask_paginate import Pagination, get_page_parameter
import templater as temple
UPLOAD_FOLDER_PRODUCTS = 'static/dashboard/uploads/products'

loadtheme_ = dataengine.knightclient()
themes = loadtheme_.themeget()

bloguser = Blueprint(
                        "bloguser", __name__, static_folder='static', static_url_path='/static/SYSTEM/default'
                        )


@bloguser.route(temple.route_blog, methods=['POST', 'GET'])
@bloguser.route(temple.route_blog+"/", methods=['POST', 'GET'])
@bloguser.route(temple.route_blog+"/<url>", methods=['POST', 'GET'])
@bloguser.route(temple.route_blog+"/<new>/<url>", methods=['POST', 'GET'])
def blog_mainview(new=None, url=None):
    """
    Blog main view
    """
    if url:
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
        blog = de.get_blog_single(url)
        cats = blog[7].split(",")
        cats_list = de.get_blog_cat_lists()
        return render_template(f"/SYSTEM/{themes}/blog.html", data=dt, mod=mod, blog=blog, cats=cats, catslist=cats_list, new=new)
    else:
        return redirect(f"/SYSTEM/{themes}/blog.html")


@bloguser.route(temple.route_blog_list, methods=['GET'])
def blog_list():
    """
    Blog posts listings
    """
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
    blogs = de.get_blog_listings()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    tt = len(blogs)
    pagination = Pagination(page=page, total=tt,
                            search=search, record_name='blogs', css_framework="bootstrap5")
    return render_template(f"/SYSTEM/{themes}/blog-list.html", data=dt, mod=mod, blogs=blogs, pagination=pagination)
