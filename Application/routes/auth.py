import os
from flask import Blueprint, redirect, render_template, request, session, flash
from utils import account_utils
from werkzeug.security import check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

bp = Blueprint("auth", __name__, url_prefix="/auth")

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        email = request.form.get("email").strip()
        username = request.form.get("username").strip()
        existing_user = account_utils.is_existing_user(email)
        if existing_user:
            flash("Email already exists.", "error")
            return render_template("register.html")

        user_id = account_utils.register_user(request.form)

        session["user_id"] = user_id
        session["username"] = username

        flash("User registeration successful.")
        return redirect("/")


@bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        email = request.form.get("email")
        user = account_utils.get_user(email)

        if not user or not check_password_hash(
            user["password_hash"], request.form.get("password")
        ):
            flash("Incorrect email or password.", "error")
            return render_template("login.html")

        flash("User login successful.")
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        account_utils.update_user_login_time(user["id"])

        return redirect("/")


@bp.route("/logout")
def logout():
    session.clear()
    flash("User logged out.")
    return redirect("/auth/login")
