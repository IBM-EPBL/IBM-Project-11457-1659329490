import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import convertSQLToDict
from utils import categories_utils, payer_utils

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


def register_user(form_data):
    username = form_data.get("username").strip()
    password = form_data.get("password")
    password_hash = generate_password_hash(password)
    now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    db.execute(
        "INSERT INTO users (username, password_hash, register_date, last_login) VALUES (:username, :password_hash, :register_date, :last_login)",
        {
            "username": username,
            "password_hash": password_hash,
            "register_date": now,
            "last_login": now,
        },
    )
    db.commit()
    user_id = db.execute("SELECT id from users order by ROWID DESC limit 1").fetchone()[
        0
    ]

    categories_utils.populate_default_categories(user_id)

    # create default payer
    payer_utils.add_payer(username, user_id)

    return user_id


def is_existing_user(username):
    account = db.execute(
        "SELECT username FROM users WHERE LOWER(username) = :username",
        {"username": username.lower()},
    ).fetchone()

    return True if account else False


def get_income(user_id):
    income = db.execute(
        "SELECT income FROM users WHERE id = :user_id", {"user_id": user_id}
    ).fetchone()[0]

    return float(income)
