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


def get_total_year_spendings(userID):
    results = db.execute(
        "SELECT SUM(amount) AS expenses_year FROM expenses WHERE user_id = :usersID AND strftime('%Y', date(expenseDate)) = strftime('%Y', CURRENT_DATE)",
        {"usersID": userID},
    ).fetchall()

    total_year_spending = convertSQLToDict(results)

    return total_year_spending[0]["expenses_year"]
