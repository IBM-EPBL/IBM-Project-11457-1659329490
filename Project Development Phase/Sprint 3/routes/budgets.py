import os
import json
from datetime import datetime
from flask import (
    Blueprint,
    flash,
    render_template,
    request,
    session,
)
from helpers import login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from utils import account_utils, budget_utils, categories_utils

bp = Blueprint("budgets", __name__, url_prefix="/budgets")

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


@bp.route("/view", methods=["GET", "POST"])
@login_required
def view_budgets():
    year = str(datetime.now().year)
    income = account_utils.get_income(session["user_id"])
    budgets = budget_utils.get_budgets(session["user_id"], year)
    budgeted = budget_utils.get_total_budgeted_amount(session["user_id"])
    unbudgeted_amount = income - budgeted if income >= budgeted else 0

    return render_template(
        "view_budgets.html", budgets=budgets, unbudgeted_amount=unbudgeted_amount
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_budget():
    if request.method == "POST":
        formData = dict(request.form)
        formData["categories"] = json.loads(formData["categories"])
        budget_utils.create_budget(formData, session["user_id"])
        flash("Budget created successfully")

    income = account_utils.get_income(session["user_id"])
    budgeted = budget_utils.get_total_budgeted_amount(session["user_id"])
    unbudgeted_amount = income - budgeted if income >= budgeted else 0
    categories = categories_utils.get_user_categories(session["user_id"])

    return render_template(
        "create_budget.html",
        categories=categories,
        unbudgeted=unbudgeted_amount,
    )
