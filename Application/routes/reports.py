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
from utils import reports_utils

bp = Blueprint("reports", __name__, url_prefix="/reports")

engine = create_engine(
    os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}
)
db = scoped_session(sessionmaker(bind=engine))


@bp.route("/monthly", methods=["GET"])
@login_required
def monthlyreport():
    year = str(datetime.now().year)

    monthly_report = reports_utils.get_monthly_report(session["user_id"], year)

    return render_template(
        "monthly_report.html", monthly_report=monthly_report, year=year
    )
