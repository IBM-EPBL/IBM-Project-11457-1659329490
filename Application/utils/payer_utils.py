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
        "SELECT name FROM payers WHERE user_id = :user_id",
        {"user_id": user_id},
    ).fetchall()
    payers = convertSQLToDict(results)

    return payers
