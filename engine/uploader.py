from flask import Blueprint, render_template, request, redirect, g, flash, send_from_directory, jsonify, session
import dataengine
from werkzeug.utils import secure_filename
import os
from flask_paginate import Pagination, get_page_parameter
import templater as temple

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


@uploader.route('/upload', methods=['POST'])
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
