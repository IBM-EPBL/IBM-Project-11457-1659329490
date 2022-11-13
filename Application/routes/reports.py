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
def monthly_report():
    year = str(datetime.now().year)

    monthly_report = reports_utils.get_monthly_report(session["user_id"], year)

    return render_template(
        "monthly_report.html", monthly_report=monthly_report, year=year
    )


@bp.route("/budgets", methods=["GET"])
@login_required
def budgets_report(year=None):
    year = str(datetime.now().year)

    budget_reports = reports_utils.get_budgets_report(session["user_id"], year)

    return render_template("budgets_report.html", budget_reports=budget_reports)


@bp.route("/payers", methods=["GET"])
@login_required
def payersreport():
    year = str(datetime.now().year)

    payers_report = reports_utils.get_payers_report(session["user_id"], year)

    return render_template("payers_report.html", payers_report=payers_report)


@bp.route("/spendings", methods=["GET"])
@login_required
def spendings_report():
    year = str(datetime.now().year)

    spending_report = reports_utils.get_spendings_report(session["user_id"], year)

    return render_template(
        "spending_report.html",
        spending_trends_chart=spending_report["chart"],
        spending_trends_table=spending_report["table"],
        categories=spending_report["categories"],
        year=year,
    )
