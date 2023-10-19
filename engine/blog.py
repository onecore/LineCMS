from flask import Blueprint, render_template, request, redirect, g
import dataengine
from flask_paginate import Pagination, get_page_parameter
import templater as temple
import os
from icecream import ic

blog = Blueprint("blog", __name__)
UPLOAD_FOLDER_BLOG = 'static/dashboard/uploads/blog'


def trydelete(image):
    try:
        os.remove(os.path.join(UPLOAD_FOLDER_BLOG, image))
        print("Deleted leftover")
    except:
        print("Trydelete except")
        pass


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
                # trydelete(blog[3])
            else:
                data['image'] = ""
                # trydelete(blog[3])

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


@blog.route("/blog-new", methods=['POST', 'GET'])
def blog_new():
    if request.method == 'POST':
        data_body = request.form.get('ckeditor')  # <--
        data_title = request.form.get('title')  # <--
        data_categ = request.form.get('cat')  # <--
        data_imgname = request.form.get('bimg')  # <--
        print(request.form)

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
