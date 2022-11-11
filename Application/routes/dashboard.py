import os
from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect
from helpers import login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from utils import (
    dashboard_utils,
    expenses_utils,
    categories_utils,
    reports_utils,
    payers_utils,
    account_utils,
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
        payers = payer_utils.getPayers(session["user_id"])

        income = account_utils.getIncome(session["user_id"])
        expenses_year = dashboard_utils.get_total_year_spendings(session["user_id"])
        expenses_month = dashboard_utils.get_total_month_spendings(session["user_id"])
        expenses_week = dashboard_utils.get_total_week_spendings(session["user_id"])

        expenses_last5 = dashboard_utils.get_last_five_expenses(session["user_id"])

        budgets = dashboard_utils.get_budgets(session["user_id"])

        weeks = dashboard_utils.get_last_four_weeks()
        spending_week = dashboard_utils.get_weekly_spendings(weeks, session["user_id"])

        spending_month = dashboard_utils.get_monthly_report_for_chart(
            session["user_id"], year
        )

        spending_trends = dashboard_utils.get_spending_trends(session["user_id"], year)

        payers_chart = reports_utils.generatePayersReport(session["user_id"], year)

        return render_template(
            "dashboard.html",
            categories=categories,
            payers=payers,
            date=date,
            income=income,
            expenses_year=expenses_year,
            expenses_month=expenses_month,
            expenses_week=expenses_week,
            expenses_last5=expenses_last5,
            budgets=budgets,
            spending_week=spending_week,
            spending_month=spending_month,
            spending_trends=spending_trends,
            payers_chart=payers_chart,
        )