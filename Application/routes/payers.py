import os
from datetime import datetime
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
)
from helpers import login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from helpers import apology
from utils import payers_utils

bp = Blueprint("payers", __name__, url_prefix="/payers")

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


@bp.route("/", methods=["GET"])
@login_required
def get_payers():
    payers = payers_utils.get_user_payers(session["user_id"])
    return render_template("view_payers.html", payers=payers)


@bp.route("/add", methods=["GET", "POST"])
@login_required
def addPayer():
    if request.method == "POST":
        formData = list(request.form.items())[0]
        name = formData[1]
        payers_utils.add_payer(name, session["user_id"])
    return render_template("add_payer.html")
