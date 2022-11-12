import os
from flask import Blueprint, render_template, request, session, redirect
from helpers import login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from utils import account_utils, profile_utils

bp = Blueprint("profile", __name__, url_prefix="/profile")

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


@bp.route("/", methods=["GET", "POST"])
@login_required
def profile():
    user = profile_utils.get_user_info(session["user_id"])

    return render_template(
        "profile.html",
        username=user["name"],
        income=user["income"],
        stats=user["stats"],
    )


@bp.route("/username", methods=["GET", "POST"])
@login_required
def update_username():
    if request.method == "POST":
        name = request.form["name"].strip()
        account_utils.update_username(name, session["user_id"])
        session["username"] = name

    return redirect("/profile")
