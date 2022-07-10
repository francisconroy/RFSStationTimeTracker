import pprint

from flask import Flask, url_for, render_template, request

app = Flask(__name__)

from markupsafe import escape
# TODO use escape to escape any user input data

@app.route("/")
def start_page():
    return render_template("index.html")

@app.route("/checkin")
def checkin():
    return render_template("checkin.html")

@app.post("/checkedin")
def checkedin():
    return f"{pprint.pformat(request.form)}"


@app.route("/checkout")
def checkout():
    return "<p>Hello, World!</p>"

@app.route("/about")
def hello_world():
    return "<p>Built by Francis Conroy 2022</p>"