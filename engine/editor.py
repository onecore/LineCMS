from flask import Blueprint, render_template, request, redirect, jsonify
# import dataengine
from helpers import checkpoint

editor = Blueprint("editor", __name__)


@editor.route("/edit",methods=['GET','POST'])
@checkpoint.onlylogged
def codeedit():
    return render_template("/dashboard/editor.html")
