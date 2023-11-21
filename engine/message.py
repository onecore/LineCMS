"""
SandCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.sandcms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
from flask import Blueprint, render_template, request, jsonify
import dataengine
from helpers import checkpoint

message = Blueprint("message", __name__)

_logger = dataengine.SandEngine()
log = _logger.log


@message.route("/messages")
def messages():
    "view - list all messages"
    
    _m = dataengine.SandEngine()
    data = _m.get_messages()
    return render_template("dashboard/messages.html", data=data)

@message.route("/inquire", methods=['POST'])
def messagerec():
    "api style - message capture"
    
    data = request.json
    json = data
    dicts = {
        'name': json['name'],
        'email': json['email'],
        'phone': json['phone'],
        'message': json['message'],
    }
    _de = dataengine.SandEngine()
    if (_de.message(dicts)):
        log("New message received")
        return jsonify({'status': True})
    else:
        log("New message failed to process")
        return jsonify({'status': False})



checkpoint.onlylogged(messages)