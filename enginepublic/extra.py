import dataengine
from ast import literal_eval as lite
from flask import Blueprint, render_template

extra = Blueprint("extra", __name__)


@extra.route("/_")
def extra_1():
    return ""

@extra.route("/__")
def extra_2():
    return ""

@extra.route("/___")
def extra_3():
    return ""

@extra.route("/____")
def extra_4():
    return ""

@extra.route("/_____")
def extra_5():
    return ""

@extra.route("/______")
def extra_6():
    return ""

