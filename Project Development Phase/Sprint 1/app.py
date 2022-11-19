from routes import (
    auth,
)

import db
from flask import Flask, render_template, redirect
from helpers import login_required, rupees, percent, title

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Custom filter
app.jinja_env.filters["rupees"] = rupees
app.jinja_env.filters["percent"] = percent
app.jinja_env.filters["title"] = title


@app.route("/")
@login_required
def index():
    return redirect("/dashboard")


@app.errorhandler(404)
def not_found(error):
    return redirect("/dashboard")


db.init_app(app)
app.register_blueprint(auth.bp)
