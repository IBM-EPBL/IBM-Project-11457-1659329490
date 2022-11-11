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
def get_budgets(user_id):
    results = db.execute(
        "SELECT id, name, year, amount FROM budgets WHERE user_id = :user_id  ORDER BY name ASC",
        {"user_id": user_id},
    ).fetchall()

    budgets_result_list = convertSQLToDict(results)

    
    budgets = []

    for budget in budgets_result_list:
        categories = get_categories_by_budget_id(budget["id"])
        budgets.append(
            {"amount": budget["amount"], "id": budget["id"], "name": budget["name"],
                "categories": categories, "year": budget["year"]}
        )

    return budgets
    

def get_categories_by_budget_id(budget_id):
    """Get all categories for a given budget id"""
    categories = db.execute(
        "SELECT categories.name, budgetCategories.amount * 100 as amount FROM budgetCategories INNER JOIN categories ON budgetCategories.category_id = categories.id WHERE budgetCategories.budgets_id = :budgetID",
        {"budgetID": budget_id},
    ).fetchall()

    return convertSQLToDict(categories)