import os
from flask import Blueprint, render_template, request, session, flash
from helpers import login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from utils import categories_utils

bp = Blueprint("categories", __name__, url_prefix="/categories")

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


@bp.route("/view", methods=["GET"])
@login_required
def get_categories():
    categories = categories_utils.get_user_categories(session["user_id"])
    return render_template("view_categories.html", categories=categories)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_category():
    if request.method == "POST":
        name = request.form["name"]
        id = categories_utils.add_category(name)
        categories_utils.add_category_to_user(id, session["user_id"])
        flash("Category created successfully.")

    return render_template("add_category.html")
