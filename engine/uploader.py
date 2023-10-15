from flask import Blueprint, render_template, request, redirect, g, flash, send_from_directory, jsonify, session
import dataengine
from werkzeug.utils import secure_filename
import os
from flask_paginate import Pagination, get_page_parameter
import templater as temple
import json
uploads_data = {}
uploader = Blueprint("uploader", __name__)

_logger = dataengine.knightclient()
log = _logger.log
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'svg', 'ico'])
UPLOAD_FOLDER = 'static/dashboard/uploads'
UPLOAD_FOLDER_PRODUCTS = 'static/dashboard/uploads/products'
UPLOAD_FOLDER_BLOG = 'static/dashboard/uploads/blog'


def allowed_file(filename) -> str:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@uploader.route("/media/<file>")
def showuploaded(file) -> str:
    return send_from_directory("static/dashboard/uploads", file)


@uploader.route("/media/blog/<file>")
def showuploaded_blog(file) -> str:
    return send_from_directory("static/dashboard/uploads/blog", file)


@uploader.route("/media/products/<folderid>/<file>")
def showuploaded_products(folderid, file) -> str:
    return send_from_directory("static/dashboard/uploads/products/"+folderid, file)


@uploader.route("/media/mainimage/<folderid>/<file>")
def showuploaded_productsmainimage(folderid, file) -> str:
    return send_from_directory("static/dashboard/uploads/products/"+folderid+"/mainimage", file)


@uploader.route("/<folderid>/variants/<file>")
@uploader.route("/media/variant/<folderid>/<file>")
def showuploaded_products_variant(folderid, file) -> str:
    return send_from_directory("static/dashboard/uploads/products/"+folderid+"/variants", file)


@uploader.route('/product-edit/upload-p-main', methods=['POST', 'GET', 'DELETE'])
@uploader.route('/upload-p-main', methods=['POST', 'GET', 'DELETE'])
def upload_file_product_main():
    """
    Main image file uploade
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
            print("Error: ", e)
            pass

        log("New Logo upload started")
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(custom_folder, filename))
            r = custom_folder+"/"+filename
            # de = dataengine.knightclient()
            # d = de.productmainupdater("mainimage", _iddc, r, filename=filename)
            return r
    elif request.method == 'DELETE':
        os.remove(os.path.join(request.data))
        print(f"DELETED IMAGE FILE: {request.data}")
        return "true"
    return jsonify({"status": "success"})


@uploader.route('/product-edit/upload-p-images', methods=['POST', 'GET', 'DELETE'])
@uploader.route('/upload-p-images', methods=['POST', 'GET', 'DELETE'])
def upload_file_product_images():
    """
    Images files upload
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
            print("Error: ", e)
            pass

        log("New Logo upload started")
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(custom_folder, filename))
            r = custom_folder+"/"+filename
            # de = dataengine.knightclient()
            # d = de.productimagesupdater("images", _iddc, r, filename)
            return r
    elif request.method == 'DELETE':
        os.remove(os.path.join(request.data))
        print(f"DELETED IMAGE FILE: {request.data}")
        return "true"
    return jsonify({"status": "success"})


@uploader.route('/product-edit/upload-p-variant', methods=['POST', 'GET', 'DELETE'])
@uploader.route('/upload-p-variant', methods=['POST', 'GET', 'DELETE'])
def upload_file_product_variant():
    """
    File upload for variants
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
            print("Error: ", e)
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
            de = dataengine.knightclient()
            d = de.productvariantsupdater("variants", _iddc, r)
            return r

    elif request.method == 'DELETE':
        # 2 requests sends to this method (one in plain text & one in json obj) (DIY as filepond creates this bug)
        stop = 0
        ############# REMOVE VARIANT DOM (contains json)
        # try:
        #     jsobj = json.loads(request.data)
        #     if 'filev' in jsobj:
        #         _rf = UPLOAD_FOLDER_PRODUCTS+"/" + \
        #             str(jsobj['fid'])+"/variants/"+jsobj['filev']
        #         os.remove(os.path.join(_rf))
        #         stop = 1
        #         return ""
        # except Exception as e:
        #     print("Cant delete", e)

        ############# FILEPOND DELETE (contains PATH ONLY)
        if not stop:
            try:
                os.remove(os.path.join(request.data))
                print(f"DELETED IMAGE FILE: {request.data}")
                return "true"
            except:
                return ""
    return jsonify({"status": "success"})


@uploader.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        log("New Logo upload started")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            print("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("success processing now")
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            d_e = dataengine.knightclient()
            try:
                d_e.update_data_uploads("control", "logo", filename,
                                        "owner", session['authenticated'][0])
                log("Logo file uploaded")
            except Exception as e:
                log("Logo upload failed, revert")
                # if fails, revert to sample logo
                d_e.update_data_uploads("control", "logo", 'sample.png',
                                        "owner", session['authenticated'][0])
                filename = "sample.png"
            return jsonify({"status": filename})
    return jsonify({"status": "success"})


@uploader.route('/upload-blog', methods=['POST'])
def upload_file_blog():
    print("Blog thumbnail upload")
    if request.method == 'POST':
        log("New Logo upload started")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            print("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("success processing now")
            filename = secure_filename(file.filename)

            file.save(os.path.join(UPLOAD_FOLDER_BLOG, filename))
            d_e = dataengine.knightclient()
            try:
                # d_e.update_data_uploads("control", "logo", filename,
                #                         "owner", session['authenticated'][0])
                log("Post thumbnail uploaded")
            except Exception as e:
                log("Post thumbnail failed, revert")
                # if fails, revert to sample logo
                # d_e.update_data_uploads("control", "logo", 'sample.png',
                #                         "owner", session['authenticated'][0])
                # filename = "sample.png"
            return jsonify({"status": filename})
    return jsonify({"status": "success"})


@uploader.route('/upload_fav', methods=['POST'])
def upload_fav():
    if request.method == 'POST':
        log("New Favicon file upload started")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            print("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("success processing now")
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            d_e = dataengine.knightclient()
            try:
                d_e.update_data_uploads("control", "favicon", filename,
                                        "owner", session['authenticated'][0])
                log("Favicon file uploaded")
            except Exception as e:
                log("Favicon file failed to upload: ", e)
                # if fails, revert to sample logo
                d_e.update_data_uploads("control", "favicon", 'knight.svg',
                                        "owner", session['authenticated'][0])
                filename = "knight.svg"
            return jsonify({"status": filename})
    return jsonify({"status": "success"})
