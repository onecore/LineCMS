from flask import Blueprint, render_template, request, redirect, g, session, jsonify
import dataengine
from flask_paginate import Pagination, get_page_parameter
import templater as temple

_logger = dataengine.knightclient()
log = _logger.log

api = Blueprint("api", __name__)
version = "1.4"


@api.route("/product-api-partial/<data>", methods=['POST', 'GET'])
def productpartial(data):
    pass


@api.route("/module_update", methods=['POST', 'GET'])
def modupdate():
    if request.method == "POST":
        if 'authenticated' in session:  # Logged in
            de = dataengine.knightclient()
            print(">>>>>> ", request.data)
            if (de.update_module(request.data)):
                return jsonify({'status': True})
            else:
                return jsonify({'status': False})
        return "KnightStudio Dashboard build ", version
    else:
        return "KnightStudio Dashboard build ", version


@api.route("/knightclientapi", methods=['POST', 'GET'])
def knightapi():
    if request.method == "POST":
        if 'authenticated' in session:  # Logged in
            d = dataengine.knightclient()
            if (d.knightclientapi(eval(request.data)['action'])):
                log("API Call success")
                return jsonify({'status': True})
            else:
                log("API Call failed")
                return jsonify({'status': False})
        return "KnightStudio Dashboard build ", version
    else:
        return "KnightStudio Dashboard build ", version


@api.route("/deleapi", methods=['POST', 'GET'])
def delete_api():
    if request.method == "POST":
        if 'authenticated' in session:  # Logged in
            table = request.json['table']
            column = request.json['column']
            value = request.json['value']
            de = dataengine.knightclient()
            if (de.delete_api(table, column, value)):
                return jsonify({"status": 1, "message": "Blog post has been deleted"})
            else:
                return jsonify({"status": 1, "message": "Blog post cannot delete right now"})
    else:
        return jsonify({"status": 0})


@api.route("/knightclientapiv2", methods=['POST', 'GET'])
def knightapi2():
    if request.method == "POST":
        if 'authenticated' in session:  # Logged in
            d = dataengine.knightclient()
            if (d.knightclientapiv2(eval(request.data))):
                print(request.data)
                log("API Call success")
                return jsonify({'status': True})
            else:
                log("API Call failed")
                return jsonify({'status': False})
        return "KnightStudio Dashboard build ", version
    else:
        return "KnightStudio Dashboard build ", version


@api.route("/delete/<table>/<id>")
def delete(table, id):
    mid = id
    if 'authenticated' in session:
        d = dataengine.knightclient()
        if d.delete(table, id):
            return jsonify({"status": True})
        else:
            return jsonify("status", False)
    return jsonify({"status": False})