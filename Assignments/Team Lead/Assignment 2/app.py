from . import db, auth
from flask import Flask, render_template
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


db.init_app(app)
app.register_blueprint(auth.bp)
