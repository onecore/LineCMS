from flask import Blueprint, render_template, request, redirect, g, session, url_for, jsonify
import dataengine
from flask_paginate import Pagination, get_page_parameter
import templater as temple

message = Blueprint("message", __name__)

_logger = dataengine.knightclient()
log = _logger.log


@message.route("/messages")
def messages():
    _m = dataengine.knightclient()
    data = _m.get_messages()
    return render_template("dashboard/messages.html", data=data)


@message.route("/inquire", methods=['POST'])
def messagerec():
    data = request.json
    json = data
    dicts = {
        'name': json['name'],
        'email': json['email'],
        'phone': json['phone'],
        'message': json['message'],
    }
    _de = dataengine.knightclient()
    if (_de.message(dicts)):
        log("New message from received")
        return jsonify({'status': True})
    else:
        log("New message failed to process")
        return jsonify({'status': False})
