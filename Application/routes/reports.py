import os
from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    session,
)
from helpers import login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from helpers import apology
from utils import reports_utils

bp = Blueprint("reports", __name__, url_prefix="/reports")

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))
