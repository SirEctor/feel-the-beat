from flask import Flask, render_template, request, flash, url_for, redirect, session
from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    login_user,
    logout_user,
    current_user,
)
import requests
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import urllib.parse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.urls import url_parse


from datetime import date
from datetime import datetime

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}".format(
    user=os.getenv("POSTGRES_USER"),
    passwd=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=5432,
    table=os.getenv("POSTGRES_DB"),
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .table_datatypes import *
from .util import *
from .api import *

login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=int(id)).first()


@app.route("/")
def home():
    logout_user()

    return render_template("index.html")


@app.route("/login")
def login():
    if current_user.is_authenticated:
        return render_template("index.html")
    return render_template("login.html")


@app.route("/register")
def register():
    if current_user.is_authenticated:
        return render_template("index.html")
    return render_template("register.html")


@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    if request.method == "POST":
        uname = request.form.get("uname")
        psw = request.form.get("psw")
        msg = None

        if not uname:
            msg = "Username is required."
        elif not psw:
            msg = "Password is required."
        elif User.query.filter_by(username=uname).first() is not None:
            msg = f"User {uname} is already registered."

        if not msg:
            new_user = User(username=uname, password=generate_password_hash(psw))
            session["username"] = new_user.username
            session["password"] = new_user.password
            db.session.add(new_user)
            db.session.commit()

            BASE_URL = "https://accounts.spotify.com/authorize"

            url_parameters = {
                "client_id": os.getenv("CLIENT_ID"),
                "response_type": "code",
                "redirect_uri": os.getenv("REDIRECT_URI"),
                "scope": "user-read-private,user-read-recently-played",
            }

            url = BASE_URL + "?" + urllib.parse.urlencode(url_parameters)
            return redirect(url)

        flash(msg)
        return render_template("register.html")


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        user_id = current_user.id
        mood = request.form["radioe"]
        song_uri = request.form["songRadio"]
        dt = date.today()
        dat = datetime.combine(dt, datetime.min.time())
        entry = Daily_Record(user_id=user_id, mood=mood, song_uri=song_uri, date=dat)

        db.session.add(entry)
        db.session.commit()
    flash("Your mood and song are saved!")
    return render_template("dashboard.html")


@app.route("/confirm_login", methods=["POST"])
def confirm_login():
    if request.method == "POST":
        uname = request.form.get("uname")
        psw = request.form.get("psw")
        msg = None
        user = User.query.filter_by(username=uname).first()

        if not uname:
            msg = "Username is required."
        elif not uname:
            msg = "Password is required."

        if user is None:
            msg = "Incorrect username."
        elif not check_password_hash(user.password, psw):
            msg = "Incorrect password."

        if not msg:
            msg = "Login Successful"
            login_user(user)
            next_page = request.args.get("next")
            if not next_page or url_parse(next_page).netloc != "":
                refreshToken = user.give_refresh_token()

                data = {
                    "client_id": os.getenv("CLIENT_ID"),
                    "client_secret": os.getenv("CLIENT_SECRET"),
                    "grant_type": "refresh_token",
                    "refresh_token": refreshToken,
                    "redirect_uri": os.getenv("REDIRECT_URI"),
                }

                r = requests.post("https://accounts.spotify.com/api/token", data=data)
                return error_handling(r, "confirm_login")

            return redirect(next_page)
        flash(msg)
        return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    if "code" in request.url:
        equalIndex = request.url.index("=")
        authorization_code = request.url[equalIndex + 1 :]
        currentUser = User.query.filter_by(username=session.get("username")).first()

        session["authorization_code"] = authorization_code
        currentUser.set_auth_code(authorization_code)
        db.session.commit()
        login_user(currentUser)
        return redirect("/test_analytics")

    return render_template("dashboard.html")


@app.route("/test_analytics")
def test_analytics():
    authorization_code = session["authorization_code"]
    data = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": os.getenv("REDIRECT_URI"),
    }
    r = requests.post("https://accounts.spotify.com/api/token", data=data)
    return error_handling(r, "test_analytics")


@app.route("/submit_mood")
def submit_mood_song():
    if "code" in request.url:
        equalIndex = request.url.index("=")
        authorization_code = request.url[equalIndex + 1 :]
        currentUser = User.query.filter_by(username=session.get("username")).first()

        session["authorization_code"] = authorization_code
        currentUser.set_auth_code(authorization_code)
        db.session.commit()
        login_user(currentUser)
        return redirect("/test_analytics")
    return render_template("dashboard.html")
