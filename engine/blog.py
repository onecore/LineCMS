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
    de = dataengine.SandEngine()
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
    showpager = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    offset = (page - 1) * int(per_page)


    de = dataengine.SandEngine()
    search = False
    q = request.args.get('q')
    if q:
        search = True

    blog = de.get_blog_listings(quer=[offset,per_page])
    tcount =  de.get_blog_listings(getcount=True)[0]



    pagination = Pagination(page=page, total=tcount,
                            search=search, record_name='blog', css_framework="bootstrap5",alignment="center")
    return render_template("/dashboard/blog-manage.html", blog=blog, pagination=pagination, alert=alert)


@blog.route("/blog-new", methods=['POST', 'GET'])
def blog_new():
    "view - publish new blog "
    if request.method == 'POST':
        de = dataengine.SandEngine()
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
