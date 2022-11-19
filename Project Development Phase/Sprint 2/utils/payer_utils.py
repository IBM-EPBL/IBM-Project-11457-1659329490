import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from helpers import convertSQLToDict

# Create engine object to manage connections to DB, and scoped session to separate user interactions with DB
engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


def add_payer(name, user_id):
    db.execute(
        "INSERT INTO payers (user_id,name) VALUES (:user_id,:name)",
        {"name": name, "user_id": user_id},
    )
    db.commit()


def get_user_payers(user_id):
    results = db.execute(
        "SELECT id, name FROM payers WHERE user_id = :user_id",
        {"user_id": user_id},
    ).fetchall()
    payers = convertSQLToDict(results)

    return payers


def get_payers_and_amount_spent(user_id, year):
    payers = []

    payers_with_expenses_results = db.execute(
        "SELECT payers.name AS name, SUM(amount) AS amount FROM expenses JOIN payers ON payers.id = expenses.payer_id WHERE expenses.user_id = :user_id AND strftime('%Y', date(date)) = :year GROUP BY payer_id ORDER BY amount DESC",
        {"user_id": user_id, "year": year},
    ).fetchall()

    payer_with_expenses = convertSQLToDict(payers_with_expenses_results)
    for payer in payer_with_expenses:
        payer["name"] = payer["name"].title()
        payers.append(payer)

    payers_without_expenses_result = db.execute(
        "SELECT name FROM payers WHERE user_id = :user_id AND id NOT IN (SELECT payer_id FROM expenses WHERE expenses.user_id = :user_id AND strftime('%Y', date(date)) = :year)",
        {"user_id": user_id, "year": year},
    ).fetchall()
    payers_without_expenses = convertSQLToDict(payers_without_expenses_result)
    for payer in payers_without_expenses:
        payers.append({"name": payer["name"].title(), "amount": 0})

    return payers
