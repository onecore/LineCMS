"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
import settings
import dataengine
from helpers import dataparser
from ast import literal_eval as lite
from flask import Blueprint, render_template, make_response,request

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
    sitedata = dataparser.Obj("site",de.load_data_index(True))
    print(sitedata.sitename)

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

    blog_posts,products_posts = [],[]

    if blog_posts_tp:
        for post in blog_posts_tp:
            if post[6] and post[5] == "0":
                blog_posts.append(post[6])

    if products_posts_tp:
        for product in products_posts_tp:
            if product[12] == "0":
                products_posts.append(product[4] or product[5])

    if not settings.sitemap_blogcategory:
        blog_categories = False

    if not settings.sitemap_blogposts:
        blog_posts = False
    
    if not settings.sitemap_productscategory:
        products_categories = False

    if not settings.sitemap_productsposts:
        products_posts = False

    sitemap_xml = render_template("/sitemap.xml",host=host,
                                  blog_cats=blog_categories,blog_posts=blog_posts,
                                  products_cats=products_categories,products_posts=products_posts)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"    
    return response

@mains.route("/robots.txt")
def robots():
    "views - generated robots file"
    robots_file = render_template("robots.txt",host=request.host_url)
    response = make_response(robots_file)
    response.headers["Content-Type"] = "text/plain"    
    return response