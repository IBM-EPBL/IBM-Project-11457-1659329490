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
        "SELECT categories.id, categories.name FROM usercategories INNER JOIN categories ON usercategories.category_id = categories.id WHERE usercategories.user_id = :user_id",
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
