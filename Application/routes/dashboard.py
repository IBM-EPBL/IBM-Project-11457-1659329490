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
    # User reached route via GET
    if request.method == "GET":
        # Initialize metrics to None to render the appropriate UX if data does not exist yet for the user
        expenses_year = None
        expenses_month = None
        expenses_week = None
        expenses_last5 = None
        spending_week = []
        spending_month = []
        year = str(datetime.now().year)
        # Get the users spend categories (for quick expense modal)
        categories = categories_utils.get_user_categories(session["user_id"])

        # Get the users payers (for quick expense modal)
        payers = account_utils.getPayers(session["user_id"])

        # Get todays date (for quick expense modal)
        date = datetime.today().strftime("%Y-%m-%d")

        # Get the users income
        income = account_utils.getIncome(session["user_id"])

        # Get current years total expenses for the user
        expenses_year = dashboard_utils.getTotalSpend_Year(session["user_id"])

        # Get current months total expenses for the user
        expenses_month = dashboard_utils.getTotalSpend_Month(session["user_id"])

        # # Get current week total expenses for the user
        expenses_week = dashboard_utils.getTotalSpend_Week(session["user_id"])

        # Get last 5 expenses for the user
        expenses_last5 = dashboard_utils.getLastFiveExpenses(session["user_id"])

        # Get every budgets spent/remaining for the user
        budgets = dashboard_utils.getBudgets(session["user_id"])

        # Get weekly spending for the user
        weeks = dashboard_utils.getLastFourWeekNames()
        spending_week = dashboard_utils.getWeeklySpending(weeks, session["user_id"])

        # Get monthly spending for the user (for the current year)
        spending_month = dashboard_utils.get_monthly_report_for_chart(
            session["user_id"], year
        )

        # Get spending trends for the user
        spending_trends = dashboard_utils.getSpendingTrends(session["user_id"], year)

        # Get payer spending for the user
        payersChart = reports_utils.generatePayersReport(session["user_id"], year)

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
            payersChart=payersChart,
        )

    # User reached route via POST
    else:
        # Get all of the expenses provided from the HTML form
        formData = list(request.form.items())

        # Add expenses to the DB for user
        expenses = expenses_utils.addExpenses(formData, session["user_id"])

        # Redirect to results page and render a summary of the submitted expenses
        return redirect("/dashboard")
