import os
from datetime import datetime
from flask import Blueprint, render_template, request, session, flash
from helpers import login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from utils import expenses_utils, categories_utils, payer_utils, budget_utils

bp = Blueprint("expenses", __name__, url_prefix="/expenses")

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_expense():
    # User reached route via POST
    if request.method == "POST":
        formData = dict(request.form.items())
        expenses_utils.add_expense(formData, session["user_id"])
        flash("Expense added successfully")

    categories = categories_utils.get_user_categories(session["user_id"])
    payers = payer_utils.get_user_payers(session["user_id"])
    budgets = budget_utils.get_budgets(session["user_id"])

    date = datetime.today().strftime("%Y-%m-%d")

    return render_template(
        "add_expenses.html",
        categories=categories,
        date=date,
        payers=payers,
        budgets=budgets,
    )


@bp.route("/view", methods=["GET"])
@login_required
def get_expenses():
    expenses = expenses_utils.get_expenses(session["user_id"])

    return render_template(
        "view_expenses.html",
        expenses=expenses,
    )
