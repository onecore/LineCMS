"""
SandCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.sandcms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
from flask import Blueprint, render_template, make_response,request
import dataengine
from ast import literal_eval as lite
from helpers import dataparser
import settings

mains = Blueprint("mains", __name__)

de = dataengine.SandEngine()
log = de.log
themes = de.themeget()[0]

@mains.route("/")
@mains.route("/index")
@mains.route("/main")
def main():
    """
    main page / index
    """
    dt = de.load_data_index(None)  # loads datas
    sitedata = dataparser.Site("site",de.load_data_index(True))

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
    
    return render_template(f"/SYSTEM/{themes}/index.html", data=dt, mod=mod,site=sitedata)

@mains.route("/sitemap.xml")
def sitemap():
    "views - generated sitemap file"
    host = request.host_url
    blog_categories = de.get_blog_cat_lists()
    blog_posts_tp = de.get_blog_listings()
    products_posts_tp = de.get_product_listings()
    products_categories = de.get_products_cat_lists()

    blog_posts = []

    if blog_posts_tp:
        for post in blog_posts_tp:
            if post[6] and post[5] == "0":
                blog_posts.append(post)


    if not settings.sitemap_blogcategory:
        blog_categories = False
    if not settings.sitemap_blogposts:
        blog_posts = False

    sitemap_xml = render_template("/sitemap.xml",host=host,
                                  blog_cats=blog_categories,blog_posts=blog_posts,
                                  products_cats=products_categories)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"    
    return response

@mains.route("/robots.txt")
def robots():
    "views - generated robots file"
    pass
