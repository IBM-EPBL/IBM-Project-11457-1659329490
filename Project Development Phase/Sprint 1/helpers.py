import decimal

from flask import redirect, session
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/auth/login")
        return f(*args, **kwargs)

    return decorated_function


def rupees(value):
    return f"₹{int(value)}"

def percent(value):
    return f"{int(value)}%"

def title(value):
    return value.title()


def convertSQLToDict(listOfRowProxy):
    rows = [dict(row) for row in listOfRowProxy]
    for row in rows:
        for column in row:
            if type(row[column]) is decimal.Decimal:
                row[column] = float(row[column])

    return rows
