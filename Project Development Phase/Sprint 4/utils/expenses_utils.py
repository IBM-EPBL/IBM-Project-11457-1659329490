import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from helpers import convertSQLToDict

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


def add_expense(form_data, user_id):
    expense = {
        "description": None,
        "category": None,
        "date": None,
        "amount": None,
        "payer": None,
    }

    expense["description"] = form_data["description"].strip()
    expense["category"] = form_data["category"]
    expense["date"] = form_data["date"]
    expense["payer"] = form_data["payer"]
    expense["budget"] = None if form_data["budget"] == "-1" else form_data["budget"]
    expense["amount"] = float(form_data["amount"])

    now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    db.execute(
        "INSERT INTO expenses (description, category_id, date, amount, payer_id, submit_time, user_id, budget_id) VALUES (:description, :category_id, :date, :amount, :payer_id, :submit_time, :user_id, :budget_id)",
        {
            "description": expense["description"],
            "category_id": expense["category"],
            "date": expense["date"],
            "amount": expense["amount"],
            "payer_id": expense["payer"],
            "submit_time": now,
            "user_id": user_id,
            "budget_id": expense["budget"],
        },
    )
    db.commit()

    return expense


def get_expenses(user_id):
    result = db.execute(
        "SELECT description, categories.name as category , date, payers.name as payer, IFNULL(budgets.name, '-') as budget, expenses.amount as amount FROM expenses JOIN categories on categories.id = expenses.category_id JOIN payers on payers.id = expenses.payer_id LEFT OUTER JOIN budgets on budgets.id = expenses.budget_id WHERE expenses.user_id = :user_id ORDER BY expenses.id DESC",
        {"user_id": user_id},
    ).fetchall()

    expenses = convertSQLToDict(result)
    return expenses


def get_last_n_expenses(n, user_id):
    result = db.execute(
        "SELECT description, categories.name as category , date, payers.name as payer, IFNULL(budgets.name, '-') as budget, expenses.amount as amount FROM expenses JOIN categories on categories.id = expenses.category_id JOIN payers on payers.id = expenses.payer_id LEFT OUTER JOIN budgets ON budgets.id = expenses.budget_id WHERE expenses.user_id = :user_id ORDER BY expenses.id DESC LIMIT :n",
        {"user_id": user_id, "n": n},
    ).fetchall()

    expenses = convertSQLToDict(result)
    return expenses


def get_expenses_by_budget(budget_id):
    result = db.execute(
        "SELECT description, categories.name as category , date, payers.name as payer, IFNULL(budgets.name, '-') as budget, expenses.amount as amount FROM expenses JOIN categories on categories.id = expenses.category_id JOIN payers on payers.id = expenses.payer_id LEFT OUTER JOIN budgets ON budgets.id = expenses.budget_id WHERE expenses.budget_id = :budget_id ORDER BY expenses.id",
        {"budget_id": budget_id},
    ).fetchall()

    expenses = convertSQLToDict(result)
    return expenses
