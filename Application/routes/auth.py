import os
from datetime import datetime
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
)
from utils import profile_utils
from werkzeug.security import check_password_hash, generate_password_hash
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
        # check if the user already exist
        username = request.form.get("username").strip()
        existing_user = profile_utils.is_existing_user(username)
        if existing_user:
            return render_template("register.html", username=username)

        user_id = profile_utils.register_user(request.form)

        # add user to session for login.
        session["user_id"] = user_id
        session["username"] = username

        return redirect("/")


@bp.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        # Query database for username
        username = request.form.get("username")
        user = profile_utils.get_user(username)

        if not user or not check_password_hash(
            user["password_hash"], request.form.get("password")
        ):
            return "wrong password or username"

        # add user to session for login.
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        # Record the login time
        profile_utils.update_user_login_time(session["user_id"])

        # Redirect user to home page
        return redirect("/")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
