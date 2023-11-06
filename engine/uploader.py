"""
SandCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.sandcms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
from flask import Blueprint, request, redirect, flash, send_from_directory, jsonify, session
import dataengine
from werkzeug.utils import secure_filename
import os
import json

uploads_data = {}
uploader = Blueprint("uploader", __name__)
from settings import uploads_allowedext
de = dataengine.SandEngine()
log = de.log
ALLOWED_EXTENSIONS = uploads_allowedext
UPLOAD_FOLDER = 'static/dashboard/uploads'
UPLOAD_FOLDER_PRODUCTS = 'static/dashboard/uploads/products'
UPLOAD_FOLDER_BLOG = 'static/dashboard/uploads/blog'


def allowed_file(filename) -> str:
    "validates file extension"
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@uploader.route("/media/<file>")
def showuploaded(file) -> str:
    "return uploaded -> root"
    return send_from_directory("static/dashboard/uploads", file)


@uploader.route("/media/blog/<file>")
def showuploaded_blog(file) -> str:
    "return uploaded -> blog"
    return send_from_directory("static/dashboard/uploads/blog", file)


@uploader.route("/media/products/<folderid>/<file>")
def showuploaded_products(folderid, file) -> str:
    "return uploaded -> product images"
    return send_from_directory("static/dashboard/uploads/products/"+folderid, file)


@uploader.route("/media/mainimage/<folderid>/<file>")
def showuploaded_productsmainimage(folderid, file) -> str:
    "return uploaded -> product main image"
    return send_from_directory("static/dashboard/uploads/products/"+folderid+"/mainimage", file)


# added for lightslider images / variants
@uploader.route("/<folderid>/variants/<file>")
@uploader.route("/media/variant/<folderid>/<file>")
def showuploaded_products_variant(folderid, file) -> str:
    "return uploaded -> variant image"
    return send_from_directory("static/dashboard/uploads/products/"+folderid+"/variants", file)


@uploader.route('/product-edit/upload-p-main', methods=['POST', 'GET', 'DELETE'])
@uploader.route('/upload-p-main', methods=['POST', 'GET', 'DELETE'])
def upload_file_product_main():
    """
    main image file upload
    """
    if request.method == 'POST':
        _id = None
        _iddc = dict(request.form)
        fd = dict(_iddc)['file']
        _iddc = (json.loads(fd))  # js to py dict
        try:
            if _iddc['p_id']:
                _id = _iddc['p_id']
            else:
                return False
        except:
            return False
        custom_folder = os.path.join(
            UPLOAD_FOLDER_PRODUCTS, str(_id)+"/mainimage")
        try:
            if not os.path.exists(custom_folder):
                os.makedirs(custom_folder)
        except Exception as e:
            pass

        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(custom_folder, filename))
            r = custom_folder+"/"+filename
            return r
        
    elif request.method == 'DELETE':
        os.remove(os.path.join(request.data))
        return "true"
    
    return jsonify({"status": "success"})


@uploader.route('/product-edit/upload-p-images', methods=['POST', 'GET', 'DELETE'])
@uploader.route('/upload-p-images', methods=['POST', 'GET', 'DELETE'])
def upload_file_product_images():
    """
    images files upload
    """
    if request.method == 'POST':
        _id = None
        _iddc = dict(request.form)
        fd = dict(_iddc)['file']
        _iddc = (json.loads(fd))  # js to py dict
        try:
            if _iddc['p_id']:
                _id = _iddc['p_id']
            else:
                return False
        except:
            return False
        custom_folder = os.path.join(UPLOAD_FOLDER_PRODUCTS, str(_id))
        try:
            if not os.path.exists(custom_folder):
                os.makedirs(custom_folder)
        except Exception as e:
            pass

        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(custom_folder, filename))
            r = custom_folder+"/"+filename
            return r
    elif request.method == 'DELETE':
        os.remove(os.path.join(request.data))
        return "true"
    return jsonify({"status": "success"})


@uploader.route('/product-edit/upload-p-variant', methods=['POST', 'GET', 'DELETE'])
@uploader.route('/upload-p-variant', methods=['POST', 'GET', 'DELETE'])
def upload_file_product_variant():
    """
    file upload for variants
    """
    if request.method == 'POST':
        _iddc = dict(request.form)
        _id = None
        keys = list(_iddc.keys())[0]
        fd = dict(_iddc)[keys]
        _iddc = (json.loads(fd))  # js to py dict
        try:
            if _iddc['p_id']:
                _id = _iddc['p_id']
            else:
                return False
        except:
            return False
        custom_folder = os.path.join(
            UPLOAD_FOLDER_PRODUCTS, str(_id)+"/variants")
        try:
            if not os.path.exists(custom_folder):
                os.makedirs(custom_folder)
        except Exception as e:
            pass

        if keys not in request.files:
            return redirect(request.url)
        file = request.files[keys]
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(custom_folder, filename))
            r = custom_folder+"/"+filename
            # insert in database (append or replace value)
            d = de.productvariantsupdater("variants", _iddc, r)
            return r

    elif request.method == 'DELETE':
        # 2 requests sends to this method (one in plain text & one in json obj) (DIY as filepond creates this bug or just misconfigured)
        stop = 0
        if not stop:
            try:
                os.remove(os.path.join(request.data))
                return "true"
            except:
                return ""
    return jsonify({"status": "success"})


@uploader.route('/upload', methods=['POST', 'GET'])
def upload_file():
    "logo uploader"
    if request.method == 'POST':
        log("New Logo upload started")
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            try:
                de.update_data_uploads("control", "logo", filename,
                                        "owner", session['authenticated'][0])
            except Exception as e:
                # if fails, revert to sample logo
                de.update_data_uploads("control", "logo", 'sample.png',
                                        "owner", session['authenticated'][0])
                filename = "sample.png"
            return jsonify({"status": filename})
    return jsonify({"status": "success"})


@uploader.route('/blog-edit/upload-blog', methods=['POST', 'DELETE'])
@uploader.route('/upload-blog', methods=['POST', 'DELETE'])
def upload_file_blog():
    "blog thumbnail upload"
    if request.method == 'POST':
        log("New Logo upload started")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER_BLOG, filename))

            return UPLOAD_FOLDER_BLOG+"/"+filename

    elif request.method == 'DELETE':
        os.remove(os.path.join(request.data))
        return "true"
    else:
        return jsonify({"status": 0})


@uploader.route('/upload_fav', methods=['POST'])
def upload_fav():
    "favicon uploader"
    if request.method == 'POST':
        log("New Favicon file upload started")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            try:
                de.update_data_uploads("control", "favicon", filename,
                                        "owner", session['authenticated'][0])
            except Exception as e:
                # if fails, revert to sample logo
                de.update_data_uploads("control", "favicon", 'knight.svg',
                                        "owner", session['authenticated'][0])
                filename = "knight.svg"
            return jsonify({"status": filename})
    return jsonify({"status": "success"})
