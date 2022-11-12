import os
from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect
from helpers import login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from utils import (
    dashboard_utils,
    categories_utils,
    payer_utils,
    account_utils,
    budget_utils,
    expenses_utils,
)

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        year = str(datetime.now().year)
        date = datetime.today().strftime("%Y-%m-%d")

        expenses_year = None
        expenses_month = None
        expenses_week = None
        expenses_last5 = None
        spending_week = []
        spending_month = []
        categories = categories_utils.get_user_categories(session["user_id"])
        payers = payer_utils.get_user_payers(session["user_id"])
        budgets = budget_utils.get_budgets(session["user_id"])

        income = account_utils.get_income(session["user_id"])
        expenses_year = dashboard_utils.get_total_year_spendings(session["user_id"])
        expenses_month = dashboard_utils.get_total_month_spendings(session["user_id"])
        expenses_week = dashboard_utils.get_total_week_spendings(session["user_id"])

        remaining_income = income - (expenses_year if expenses_year else 0)

        expenses_last5 = expenses_utils.get_last_n_expenses(5, session["user_id"])

        weeks = dashboard_utils.get_last_four_weeks()
        spending_week = dashboard_utils.get_weekly_spendings(weeks, session["user_id"])

        spending_month = dashboard_utils.get_monthly_report(session["user_id"], year)

        spending_trends = dashboard_utils.get_spending_trends(session["user_id"], year)

        # payers_chart = reports_utils.get_payers_report(session["user_id"], year)

        return render_template(
            "dashboard.html",
            categories=categories,
            payers=payers,
            date=date,
            income=income,
            remaining_income=remaining_income,
            expenses_year=expenses_year,
            expenses_month=expenses_month,
            expenses_week=expenses_week,
            expenses_last5=expenses_last5,
            budgets=budgets,
            spending_week=spending_week,
            spending_month=spending_month,
            spending_trends=spending_trends,
            # payers_chart=payers_chart,
        )

    if request.method == "POST":
        formData = dict(request.form.items())

        expense = expenses_utils.add_expense(formData, session["user_id"])

        # Redirect to results page and render a summary of the submitted expenses
        return redirect("/dashboard")
