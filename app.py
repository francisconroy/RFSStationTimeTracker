import pprint

from flask import Flask, url_for, render_template, request, redirect

from modules import spreadsheet
from modules.oauth_login import do_login, accept_token

app = Flask(__name__)
app.config["SERVER_NAME"] = "localhost:5000"

from markupsafe import escape
# TODO use escape to escape any user input data

@app.route("/")
def start_page():
    return render_template("index.html")

@app.route("/checkin")
def checkin():
    spreadsheet.get_employee_list()


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

@app.route("/login")
def login():
    handle_uri = url_for('handle_login', _external=True)
    print(handle_uri)
    logged_in, auth_url = do_login(handle_uri)
    if not logged_in:
        return redirect(auth_url)
    else:
        return "<p>Already signed in!</p>"

@app.route("/handle_login")
def handle_login():
    accept_token(request.args["code"])
    spreadsheet.setup_service()
    return f"<p>Logged in!</p>"
