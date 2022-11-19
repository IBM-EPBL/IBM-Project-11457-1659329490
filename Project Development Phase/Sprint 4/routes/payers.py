import os
from flask import Blueprint, render_template, request, session, flash
from helpers import login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from utils import payer_utils

bp = Blueprint("payers", __name__, url_prefix="/payers")

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


@bp.route("/view", methods=["GET"])
@login_required
def get_payers():
    payers = payer_utils.get_user_payers(session["user_id"])
    return render_template("view_payers.html", payers=payers)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_payer():
    if request.method == "POST":
        name = request.form["name"]
        payer_utils.add_payer(name, session["user_id"])
        flash("Payer added successfully.")
    return render_template("add_payer.html")
