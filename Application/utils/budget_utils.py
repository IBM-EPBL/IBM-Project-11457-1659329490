import os
import re
from utils import categories_utils

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from helpers import convertSQLToDict

# Create engine object to manage connections to DB, and scoped session to separate user interactions with DB
engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


# Get the users budgets
def get_budgets(user_id, year):
    results = db.execute(
        "SELECT id, name, year, amount FROM budgets WHERE user_id = :user_id AND year = :year ORDER BY name ASC",
        {"user_id": user_id, "year": year},
    ).fetchall()

    budgets_result_list = convertSQLToDict(results)

    budgets = []

    for budget in budgets_result_list:
        categories = get_categories_by_budget_id(budget["id"])
        budgets.append(
            {
                "amount": budget["amount"],
                "id": budget["id"],
                "name": budget["name"],
                "categories": categories,
                "year": budget["year"],
            }
        )

    return budgets


def get_categories_by_budget_id(budget_id):
    categories = db.execute(
        "SELECT categories.name, budget_categories.percent_amount * 100 as amount FROM budget_categories INNER JOIN categories ON budget_categories.category_id = categories.id WHERE budget_categories.budgets_id = :budget_id",
        {"budget_id": budget_id},
    ).fetchall()

    return convertSQLToDict(categories)


def get_total_budgeted_amount(user_id):
    year = str(datetime.now().year)

    amount = db.execute(
        "SELECT SUM(amount) AS amount FROM budgets WHERE user_id = :user_id AND year = :year",
        {"user_id": user_id, "year": year},
    ).fetchone()[0]

    return amount if amount else 0


def create_budget(budget, user_id):
    year = str(datetime.now().year)
    db.execute(
        "INSERT INTO budgets (name, year, amount, user_id) VALUES (:budgetName, :budgetYear, :budgetAmount, :user_id) RETURNING id",
        {
            "budgetName": budget["name"],
            "budgetYear": year,
            "budgetAmount": budget["amount"],
            "user_id": user_id,
        },
    )
    db.commit()

    budget_id = db.execute(
        "SELECT id from budgets order by ROWID DESC limit 1"
    ).fetchone()[0]

    add_budget_categories(budget_id, budget["categories"])

    return budget


def add_budget_categories(budget_id, categories):
    for category in categories:
        db.execute(
            "INSERT INTO budget_categories (budgets_id, category_id, percent_amount) VALUES (:budget_id, :category_id, :percent_amount)",
            {
                "budget_id": budget_id,
                "category_id": category["id"],
                "percent_amount": category["percent"],
            },
        )
    db.commit()
