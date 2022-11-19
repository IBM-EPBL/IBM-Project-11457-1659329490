import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from utils import account_utils

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


def get_statistics(user_id):

    stats = {
        "register_date": None,
        "total_expenses": None,
        "total_budgets": None,
        "total_categories": None,
        "total_payers": None,
        "expense_percentage": None,
        "budgets_percentage": None,
        "categories_percentage": None,
        "payers_percentage": None,
    }

    # Get register date
    register_date = db.execute(
        "SELECT register_date FROM users WHERE id = :user_id", {"user_id": user_id}
    ).fetchone()[0]
    stats["register_date"] = register_date.split()[0]

    # Get total expenses
    total_expenses = db.execute(
        "SELECT COUNT(*) AS count FROM expenses WHERE user_id = :user_id",
        {"user_id": user_id},
    ).fetchone()[0]
    stats["total_expenses"] = total_expenses

    # Get total budgets
    total_budgets = db.execute(
        "SELECT COUNT(*) AS count FROM budgets WHERE user_id = :user_id",
        {"user_id": user_id},
    ).fetchone()[0]
    stats["total_budgets"] = total_budgets

    # Get total categories
    total_categoies = db.execute(
        "SELECT COUNT(*) AS count FROM user_categories INNER JOIN categories ON user_categories.category_id = categories.id WHERE user_categories.user_id = :user_id",
        {"user_id": user_id},
    ).fetchone()[0]
    stats["total_categories"] = total_categoies

    # Get total payers
    total_payers = db.execute(
        "SELECT COUNT(*) AS count FROM payers WHERE user_id = :user_id",
        {"user_id": user_id},
    ).fetchone()[0]
    stats["total_payers"] = total_payers

    # calculate percentage using some arbitary values
    stats["expense_percentage"] = min(100, stats["total_expenses"] / 100 * 100)
    stats["budgets_percentage"] = min(100, stats["total_budgets"] / 10 * 100)
    stats["categories_percentage"] = min(100, stats["total_categories"] / 20 * 100)
    stats["payers_percentage"] = min(100, stats["total_payers"] / 5 * 100)

    return stats


def get_user_info(user_id):
    user = {"name": None, "income": None, "stats": None}

    user["name"] = account_utils.get_username(user_id)
    user["income"] = account_utils.get_income(user_id)
    user["stats"] = get_statistics(user_id)

    return user
