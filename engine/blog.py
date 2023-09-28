from flask import Blueprint, render_template, request, redirect, g
import dataengine
from flask_paginate import Pagination, get_page_parameter
import templater as temple

blog = Blueprint("blog", __name__)


@blog.route("/blog-edit/<url>", methods=['POST', 'GET'])
def blog_edit(url):
    de = dataengine.knightclient()
    blog = de.get_blog_single(url)

    if request.method == 'POST':
        data_body = request.form.get('ckeditor')  # <--
        data_title = request.form.get('title')  # <--
        data_categ = request.form.get('cat')  # <--
        data_imgname = request.form.get('bimg')  # <--
        data_hidden = request.form.get('ishidden')  # <--
        if not data_title:
            return render_template("/dashboard/blog-edit.html", blog=blog, error="Blog title can't be empty")
        if not data_body:
            return render_template("/dashboard/blog-edit.html", blog=blog, error="Blog content can't be empty")
        else:
            data = {"title": data_title, "body": data_body,
                    "category": data_categ, "hidden": data_hidden, "route": blog[6]}
            if data_imgname:
                data["image"] = data_imgname
            else:
                data['image'] = "no-image.jpeg"
            if data_categ:
                data['category'] = data_categ
            else:
                data['category'] = 'blog'
            try:
                if (de.blog_update(data)):
                    return redirect(temple.route_blog+"/1/"+data['route'])
                else:
                    return render_template("/dashboard/blog-edit.html", blog=blog, error="Blog post failed to publish.")
            except Exception as e:
                print(e)
                return render_template("/dashboard/blog-edit.html", blog=blog, error="Blog post failed to publish.")
    return render_template("/dashboard/blog-edit.html", blog=blog)


@blog.route("/blog-manage", methods=['POST', 'GET'])
@blog.route("/blog-manage/<alert>", methods=['POST', 'GET'])
def blog_manage(alert=None):
    de = dataengine.knightclient()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    blog = de.get_blog_listings()
    tt = len(blog)
    pagination = Pagination(page=page, total=tt,
                            search=search, record_name='blog', css_framework="bootstrap5")

    return render_template("/dashboard/blog-manage.html", blog=blog, pagination=pagination, alert=alert)


@blog.route(temple.route_blog_list, methods=['GET'])
def blog_list():
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
    return render_template(temple.render_blog_list, data=dt, mod=mod, blogs=blogs, pagination=pagination)


@blog.route(temple.route_blog, methods=['POST', 'GET'])
@blog.route(temple.route_blog+"/", methods=['POST', 'GET'])
@blog.route(temple.route_blog+"/<url>", methods=['POST', 'GET'])
@blog.route(temple.route_blog+"/<new>/<url>", methods=['POST', 'GET'])
def blog_mainview(new=None, url=None):
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
        return render_template(temple.render_blog_single, data=dt, mod=mod, blog=blog, cats=cats, catslist=cats_list, new=new)
    else:
        return redirect(temple.route_blog_list)


@blog.route("/blog-new", methods=['POST', 'GET'])
def blog_new():
    if request.method == 'POST':
        data_body = request.form.get('ckeditor')  # <--
        data_title = request.form.get('title')  # <--
        data_categ = request.form.get('cat')  # <--
        data_imgname = request.form.get('bimg')  # <--
        if not data_title:
            return render_template("/dashboard/blog-new.html", error="Blog title required")
        if not data_body:
            return render_template("/dashboard/blog-new.html", error="Blog content required")
        else:
            data = {"title": data_title,
                    "body": data_body, "category": data_categ}
            if data_imgname:
                data["image"] = data_imgname
            else:
                data['image'] = "no-image.jpeg"
            if data_categ:
                data['category'] = data_categ
            else:
                data['category'] = 'blog'
            de = dataengine.knightclient()
            try:
                if (de.blog_publish(data)):
                    return redirect(temple.route_blog+"/1/"+g.new_blog_url)
                else:
                    return render_template("/dashboard/blog-new.html", error="Blog post failed to publish.")
            except Exception as e:
                print(e)
                return render_template("/dashboard/blog-new.html", error="Blog post failed to publish.")
    return render_template("/dashboard/blog-new.html")
