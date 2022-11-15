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
    reports = []
    charts = []
    report = {"table": None, "name": None, "amount": None}

    budgets = budget_utils.get_budgets(user_id, year)
    charts.extend(budgets)
    for budget in budgets:
        expenses = expenses_utils.get_expenses_by_budget(budget["id"])
        report["name"] = budget["name"]
        report["id"] = budget["id"]
        report["amount"] = budget["amount"]
        report["table"] = expenses

        reports.append(report.copy())

    return {"reports": reports, "charts": charts}


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

    months_with_data = []
    for record in month_spendings:
        month_model["name"] = calendar.month_name[int(record["month"])]
        month_model["amount"] = record["amount"]

        months_with_data.append(month_model["name"])
        monthly_report.append(month_model.copy())

    chart_data = []
    for month in calendar.month_name[1:]:
        if month not in months_with_data:
            month_model["name"] = month
            month_model["amount"] = 0
            chart_data.append(month_model.copy())
        else:
            chart_data.append(monthly_report.pop(0))

    return chart_data


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


def get_spendings_report(user_id, year):
    spending_trends_chart = get_spending_trends(user_id, year)

    categories = []
    category_model = {"name": None, "month": 0, "count": 0, "amount": 0}

    spending_trends_table = {
        "January": [],
        "February": [],
        "March": [],
        "April": [],
        "May": [],
        "June": [],
        "July": [],
        "August": [],
        "September": [],
        "October": [],
        "November": [],
        "December": [],
    }

    categories_result = categories_utils.get_user_categories(user_id)

    for category in categories_result:
        category_model["name"] = category["name"]
        categories.append(category_model.copy())

    for month in spending_trends_table.keys():
        spending_trends_table[month] = copy.deepcopy(categories)

    results = db.execute(
        "SELECT strftime('%m', date(date)) AS month, categories.name AS name, COUNT(*) AS count, SUM(amount) AS amount FROM expenses JOIN categories ON categories.id = expenses.category_id WHERE expenses.user_id = :user_id AND strftime('%Y', date(date)) = :year GROUP BY strftime('%m', date(date)), expenses.category_id ORDER BY COUNT(expenses.category_id) DESC",
        {"user_id": user_id, "year": year},
    ).fetchall()

    spending_trends_table_query = convertSQLToDict(results)

    for category_expense in spending_trends_table_query:
        month = calendar.month_name[int(category_expense["month"])]
        for category in spending_trends_table[month]:
            if category["name"] == category_expense["name"]:
                category["month"] = category_expense["month"]
                category["count"] = category_expense["count"]
                category["amount"] = category_expense["amount"]
                break

    for i in range(len(categories)):
        category_total = 0
        for month in spending_trends_table.keys():
            category_total += spending_trends_table[month][i]["amount"]
        categories[i]["amount"] = category_total

    spending_trends_report = {
        "chart": spending_trends_chart,
        "table": spending_trends_table,
        "categories": categories,
    }

    return spending_trends_report


def get_spending_trends(user_id, year):
    spending_trends = []
    category_trend = {
        "name": None,
        "series": None,
    }

    results = db.execute(
        "SELECT categories.name as name, COUNT(*) as count, SUM(amount) as amount FROM expenses JOIN categories ON categories.id = expenses.category_id WHERE user_id = :user_id AND strftime('%Y', date(date)) = :year GROUP BY category_id  ORDER BY COUNT(*) DESC",
        {"user_id": user_id, "year": year},
    ).fetchall()
    categories = convertSQLToDict(results)

    total_spent = 0
    for category_expenses in categories:
        total_spent += category_expenses["amount"]

    for category_expenses in categories:
        percentage_spent = round((category_expenses["amount"] / total_spent) * 100)
        category_trend["name"] = category_expenses["name"]
        category_trend["series"] = [
            category_expenses["amount"],
            category_expenses["count"],
            percentage_spent,
            category_expenses["name"],
        ]

        spending_trends.append(category_trend.copy())

    return spending_trends
