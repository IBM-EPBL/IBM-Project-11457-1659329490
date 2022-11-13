import os
import calendar

# from utils import budgets_utils
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from helpers import convertSQLToDict
import datetime

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


def get_total_year_spendings(user_id):
    results = db.execute(
        "SELECT SUM(amount) AS expenses_year FROM expenses WHERE user_id = :user_id AND strftime('%Y', date(date)) = strftime('%Y', CURRENT_DATE)",
        {"user_id": user_id},
    ).fetchall()

    total_year_spendings = convertSQLToDict(results)[0]["expenses_year"]

    return total_year_spendings


def get_total_month_spendings(user_id):
    results = db.execute(
        "SELECT SUM(amount) AS expenses_month FROM expenses WHERE user_id = :user_id AND strftime('%Y', date(date)) = strftime('%Y', CURRENT_DATE) AND strftime('%m', date(date)) = strftime('%m', CURRENT_DATE)",
        {"user_id": user_id},
    ).fetchall()

    total_month_spendings = convertSQLToDict(results)[0]["expenses_month"]

    return total_month_spendings


def get_total_week_spendings(user_id):
    results = db.execute(
        "SELECT SUM(amount) AS expenses_week FROM expenses WHERE user_id = :user_id AND strftime('%Y', date(date)) = strftime('%Y', CURRENT_DATE) AND strftime('%W', date(date)) = strftime('%W', CURRENT_DATE)",
        {"user_id": user_id},
    ).fetchall()

    total_week_spendings = convertSQLToDict(results)[0]["expenses_week"]

    return total_week_spendings


def week_range(date):
    start_date = date + datetime.timedelta(-date.weekday())
    end_date = start_date + datetime.timedelta(days=6)
    return {"start": start_date, "end": end_date}


def get_last_four_weeks():
    cur = datetime.datetime.now()
    weeks = []
    for i in range(4):
        weeks.append(week_range(cur - datetime.timedelta(weeks=i)))

    return weeks


def get_weekly_spendings(weeks, user_id):
    weekly_spendings = []
    week_modal = {"start": None, "end": None, "amount": None}

    for week in weeks:
        week_modal["end"] = week["end"].strftime("%b %d")
        week_modal["start"] = week["start"].strftime("%b %d")
        results = db.execute(
            "SELECT SUM(amount) AS amount FROM expenses WHERE user_id = :user_id AND strftime('%Y', date(date)) = strftime('%Y', date(:date)) AND strftime('%W', date(date)) = strftime('%W',date(:date))",
            {"user_id": user_id, "date": str(week["end"])},
        ).fetchall()
        weekly_spending = convertSQLToDict(results)[0]["amount"]

        if weekly_spending == None:
            week_modal["amount"] = 0
        else:
            week_modal["amount"] = weekly_spending

        weekly_spendings.append(week_modal.copy())

    hasExpenses = False
    for record in weekly_spendings:
        if record["amount"] != 0:
            hasExpenses = True
            break
    if hasExpenses is False:
        weekly_spendings.clear()

    return weekly_spendings


def get_spending_trends(user_id, year):
    spending_trends = []
    category_trend = {
        "name": None,
        "proportional_amount": None,
        "total_spent": None,
        "total_count": None,
    }

    results = db.execute(
        "SELECT category_id, COUNT(*) as count, SUM(amount) as amount FROM expenses WHERE user_id = :user_id AND strftime('%Y', date(date)) = :year GROUP BY category_id ORDER BY COUNT(*) DESC",
        {"user_id": user_id, "year": year},
    ).fetchall()
    categories = convertSQLToDict(results)

    total_spent = 0
    for category_expenses in categories:
        total_spent += category_expenses["amount"]

    for category_expenses in categories:
        percentage_spent = round((category_expenses["amount"] / total_spent) * 100)
        category_trend["name"] = category_expenses["category_id"]
        category_trend["percentage_spent"] = percentage_spent
        category_trend["total_spent"] = category_expenses["amount"]
        category_trend["total_count"] = category_expenses["count"]
        spending_trends.append(category_trend.copy())

    return spending_trends
