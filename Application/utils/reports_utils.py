import os
import calendar
import copy
from utils import dashboard_utils, budget_utils, categories_utils, expenses_utils


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from helpers import convertSQLToDict
from datetime import datetime

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


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
