from flask import Blueprint, render_template, request, redirect, jsonify
# import dataengine
from helpers import checkpoint

editor = Blueprint("editor", __name__)

def get_templates():
    print()

def get_robotssitemap():
    pass

@editor.route("/edit",methods=['GET','POST'])
@checkpoint.onlylogged
def codeedit():
    items = {}
    get_templates()

    return render_template("/dashboard/editor.html")
