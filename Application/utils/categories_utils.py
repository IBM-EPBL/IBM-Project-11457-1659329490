import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from helpers import convertSQLToDict

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


def get_user_categories(user_id):
    results = db.execute(
        "SELECT categories.id, categories.name FROM user_categories INNER JOIN categories ON user_categories.category_id = categories.id WHERE user_categories.user_id = :user_id",
        {"user_id": user_id},
    ).fetchall()

    categories = convertSQLToDict(results)

    return categories

def add_category(name):
    db.execute(
        "INSERT INTO categories (name) VALUES (:name)", {
            "name": name}
    )
    db.commit()
    category_id = db.execute("SELECT id from categories order by ROWID DESC limit 1").fetchone()[0]
    return category_id
    
# Adds a category to the users account
def add_category_to_user(category_id, user_id):
    db.execute(
        "INSERT INTO usercategories (user_id, category_id) VALUES (:user_id, :category_id)",
        {"user_id": user_id, "category_id": category_id},
    )
    db.commit()


def populate_default_categories(user_id):
    db.execute(
        "INSERT INTO user_categories (category_id, user_id) VALUES (1, :user_id), (2, :user_id), (3, :user_id), (4, :user_id), (5, :user_id), (6, :user_id), (7, :user_id), (8, :user_id)",
        {"user_id": user_id},
    )
    db.commit()
