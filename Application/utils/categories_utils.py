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

