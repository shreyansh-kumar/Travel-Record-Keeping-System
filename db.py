import mysql.connector
import click
from flask import current_app
from flask import g


def get_db():
    """Connect to the application's configured database. The connection is unique for each request and will be reused if this is called again."""
    if "db" not in g:
        g.db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "verybadpassword",
            port=3306,
            db="travel",
        )
        #g.db.execute(" USE travel")
        #g.db.row_factory = mysql.connector.Row

    return g.db.cursor()


def close_db(e=None):
    """If this request connected to the database, close the connection."""
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()
    #db.execute(" CREATE DATABASE travel")
    db.execute(" USE travel")
    with current_app.open_resource("schema.sql") as f:
        db.execute(f.read()) #.decode("utf8"), multi=True
    db.execute("COMMIT")


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by the application factory."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)