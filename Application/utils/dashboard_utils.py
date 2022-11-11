import os
import calendar
from utils import budgets_utils
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
        "SELECT SUM(amount) AS expenses_year FROM expenses WHERE user_id = :usersID AND strftime('%Y', date(expenseDate)) = strftime('%Y', CURRENT_DATE)",
        {"usersID": user_id},
    ).fetchall()

    total_year_spendings = convertSQLToDict(results)

    return total_year_spendings[0]["expenses_year"]


def get_total_month_spendings(user_id):
    results = db.execute(
        "SELECT SUM(amount) AS expenses_month FROM expenses WHERE user_id = :usersID AND strftime('%Y', date(expenseDate)) = strftime('%Y', CURRENT_DATE) AND strftime('%m', date(expenseDate)) = strftime('%m', CURRENT_DATE)",
        {"usersID": user_id},
    ).fetchall()

    total_month_spendings = convertSQLToDict(results)

    return total_month_spendings[0]["expenses_month"]


def get_total_week_spendings(user_id):
    results = db.execute(
        "SELECT SUM(amount) AS expenses_week FROM expenses WHERE user_id = :usersID AND strftime('%Y', date(expenseDate)) = strftime('%Y', CURRENT_DATE) AND strftime('%W', date(expenseDate)) = strftime('%W', CURRENT_DATE)",
        {"usersID": user_id},
    ).fetchall()

    total_week_spendings = convertSQLToDict(results)

    return total_week_spendings[0]["expenses_week"]
