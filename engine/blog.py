"""
SandCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.sandcms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
from flask import Blueprint, render_template, request, redirect, g
import dataengine
from flask_paginate import Pagination, get_page_parameter
import settings as temple
import os

blog = Blueprint("blog", __name__)
UPLOAD_FOLDER_BLOG = 'static/dashboard/uploads/blog'


def trydelete(image):
    """
    Deletes any image that is considered left-over, not updated in db and not needed
    """
    try:
        os.remove(os.path.join(UPLOAD_FOLDER_BLOG, image))
    except:
        pass


@blog.route("/blog-edit/<url>", methods=['POST', 'GET'])
def blog_edit(url):
    "view - blog edit"
    de = dataengine.knightclient()
    blog = de.get_blog_single(url)

    if request.method == 'POST':
        data_body = request.form.get('ckeditor') 
        data_title = request.form.get('title') 
        data_categ = request.form.get('cat') 
        data_imgname = request.form.get('bimg') 
        data_hidden = request.form.get('ishidden') 
        if not data_title:
            return render_template("/dashboard/blog-edit.html", blog=blog, error="Blog title can't be empty")
        if not data_body:
            return render_template("/dashboard/blog-edit.html", blog=blog, error="Blog content can't be empty")
        else:
            data = {"title": data_title, "body": data_body,
                    "category": data_categ, "hidden": data_hidden, "route": blog[6]}
            if data_imgname:
                data["image"] = data_imgname
                # trydelete(blog[3]) unused needs testing
            else:
                data['image'] = ""
                # trydelete(blog[3]) unused needs testing
            if data_categ:
                data['category'] = data_categ
            else:
                data['category'] = 'blog'
            try:
                if (de.blog_update(data)):
                    # /1/ pattern will show Success
                    return redirect(temple.route_blog+"/1/"+data['route'])
                else:
                    return render_template("/dashboard/blog-edit.html", blog=blog, error="Blog post failed to publish.")
            except Exception as e:
                return render_template("/dashboard/blog-edit.html", blog=blog, error="Blog post failed to publish.")
    return render_template("/dashboard/blog-edit.html", blog=blog)


@blog.route("/blog-manage", methods=['POST', 'GET'])
@blog.route("/blog-manage/<alert>", methods=['POST', 'GET'])
def blog_manage(alert=None):
    "view - lists blog posts"
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
    "view - publish new blog "
    if request.method == 'POST':
        de = dataengine.knightclient()
        data_body = request.form.get('ckeditor') 
        data_title = request.form.get('title') 
        data_categ = request.form.get('cat') 
        data_imgname = request.form.get('bimg') 

        if not data_title:
            return render_template("/dashboard/blog-new.html", error="Blog title required")
        if not data_body:
            return render_template("/dashboard/blog-new.html", error="Blog content required")
        else:
            data = {
                    "title": data_title,
                    "body": data_body,
                    "category": data_categ
                    }
            if data_imgname:
                data["image"] = data_imgname
            else:
                data['image'] = ""
            if data_categ:
                data['category'] = data_categ
            else:
                data['category'] = 'blog'
            try:
                if (de.blog_publish(data)):
                    return redirect(temple.route_blog+"/1/"+g.new_blog_url)
                return render_template("/dashboard/blog-new.html", error="Blog post failed to publish.")
            except Exception as e:
                return render_template("/dashboard/blog-new.html", error="Blog post failed to publish.")
    return render_template("/dashboard/blog-new.html")
