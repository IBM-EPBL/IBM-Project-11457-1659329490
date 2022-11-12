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


def get_user(username):
    user = db.execute(
        "SELECT * FROM users WHERE username = :username",
        {"username": username},
    ).fetchone()
    return user


def update_user_login_time(user_id):
    now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    db.execute(
        "UPDATE users SET last_login = :last_login WHERE id = :user_id",
        {"last_login": now, "user_id": user_id},
    )
    db.commit()


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


def update_username(name, user_id):
    db.execute(
        "UPDATE users SET username = :name where id = :user_id ",
        {"name": name, "user_id": user_id},
    )
    db.commit()


def get_username(user_id):
    name = db.execute(
        "SELECT username FROM users WHERE id = :user_id", {"user_id": user_id}
    ).fetchone()[0]

    return name


def get_income(user_id):
    income = db.execute(
        "SELECT income FROM users WHERE id = :user_id", {"user_id": user_id}
    ).fetchone()[0]

    return float(income)


def update_income(income, user_id):
    db.execute(
        "UPDATE users SET income = :income WHERE id = :user_id",
        {"income": income, "user_id": user_id},
    ).rowcount
    db.commit()


def update_password(old_pass, new_pass, user_id):
    password_hash_db = db.execute(
        "SELECT password_hash FROM users WHERE id = :user_id", {"user_id": user_id}
    ).fetchone()[0]

    if not check_password_hash(password_hash_db, old_pass):
        return {"error": "Current password is wrong"}

    new_hashed_password = generate_password_hash(new_pass)

    db.execute(
        "UPDATE users SET password_hash = :hashed_pass WHERE id = :user_id",
        {"hashed_pass": new_hashed_password, "user_id": user_id},
    )
    db.commit()
