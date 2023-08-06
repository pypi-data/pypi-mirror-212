from flask import Blueprint, render_template, request, g
from datetime import datetime
from utah.arches.web_blueprints import content_blueprint

app = Blueprint('myapp', __name__)

counter = 0

@app.route("/")
def hello_world():
    return content_blueprint._getDocument("main/default.html", g.locale)

@app.route("/favicon.ico")
def favicon():
    return content_blueprint._getDocument("main/images/tool-icon.png", g.locale)
