# -*- coding: utf-8 -*-
# For Cover : http://127.0.0.1:5000/Welcome/

from flask import Flask, render_template
from flask import current_app as app


@app.route("/Welcome/")
def welcome():
    return render_template("Cover.html")
