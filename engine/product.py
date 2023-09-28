from flask import Blueprint, render_template, request, redirect, g
import dataengine
from flask_paginate import Pagination, get_page_parameter
import templater as temple

product = Blueprint("product", __name__)


@product.route("/product-new", methods=['POST', 'GET'])
def product_new():
    return render_template("/dashboard/product-new.html")


@product.route("/product-manage", methods=['POST', 'GET'])
def product_mng():
    return render_template("/dashboard/product-manage.html")
