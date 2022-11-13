import os
import calendar
import copy
from utils import (
    dashboard_utils,
    budget_utils,
    categories_utils,
    expenses_utils,
    payer_utils,
)


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from helpers import convertSQLToDict
from datetime import datetime

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


def get_budgets_report(user_id, year):
    budget_reports = []
    report = {"table": None, "chart": None, "name": None, "amount": None}

    budgets = budget_utils.get_budgets(user_id, year)
    for budget in budgets:
        expenses = expenses_utils.get_expenses_by_budget(budget["id"])
        report["name"] = budget["name"]
        report["amount"] = budget["amount"]
        report["table"] = expenses

        budget_reports.append(report.copy())

    return budget_reports


def get_monthly_report(user_id, year):
    month_report_chart = get_monthly_report_chart(user_id, year)

    results = expenses_utils.get_expenses(user_id)
    monthly_report_table = convertSQLToDict(results)

    monthlyReport = {"chart": month_report_chart, "table": monthly_report_table}

    return monthlyReport


def get_monthly_report_chart(user_id, year):
    monthly_report = []
    month_model = {"name": None, "amount": None}

    results = db.execute(
        "SELECT strftime('%m', date(date)) AS month, SUM(amount) AS amount FROM expenses WHERE user_id = :user_id AND strftime('%Y', date(date)) = :year GROUP BY strftime('%m', date(date))  ORDER BY month",
        {"user_id": user_id, "year": year},
    ).fetchall()

    month_spendings = convertSQLToDict(results)

    for record in month_spendings:
        month_model["name"] = calendar.month_abbr[int(record["month"])]
        month_model["amount"] = record["amount"]

        monthly_report.append(month_model.copy())

    return monthly_report


def get_payers_report(user_id, year):
    payers_and_amount_spent = payer_utils.get_payers_and_amount_spent(user_id, year)

    total_amount_spent = 0
    for payer in payers_and_amount_spent:
        total_amount_spent = total_amount_spent + payer["amount"]

    if total_amount_spent != 0:
        for payer in payers_and_amount_spent:
            payer["percent_amount"] = round(
                (payer["amount"] / total_amount_spent) * 100
            )

    return payers_and_amount_spent
