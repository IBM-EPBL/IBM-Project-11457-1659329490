import sqlite3

import click
from flask import current_app, g


def get_db():
    db = sqlite3.connect("database.db", detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    print("Database connection created")

    return db


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

    db.close()
    print("DB connection clossed")


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.cli.add_command(init_db_command)
