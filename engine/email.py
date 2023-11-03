from flask import Blueprint, render_template, request, redirect, g, session, url_for
import dataengine
from flask_paginate import Pagination, get_page_parameter

email = Blueprint("email", __name__)

_logger = dataengine.knightclient()
log = _logger.log

