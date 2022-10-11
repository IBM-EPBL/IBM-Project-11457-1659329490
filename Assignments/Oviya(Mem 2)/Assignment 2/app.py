from . import db, auth
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "oviii"


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


db.init_app(app)
app.register_blueprint(auth.bp)
