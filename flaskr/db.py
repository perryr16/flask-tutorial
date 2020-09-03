    # g is a special pbject that is uniqe for each request. its reused if get_db is called
      # current_app special object. points to the Flask app handling the req.
    # return the db rows that will act like dicts (hash?)
    # allows accessing the columns by name
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

  # get_db returns a database connection
  # open resource opens a file relative to the flaskr package. 
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# defines a cli command called init-db. show a success message
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

  # tells flask to call that fxn when cleaning up after a response
  # adds a new command that can be called with the `flask` command 
def init_app(app):
  app.teardown_appcontext(close_db)
  app.cli.add_command(init_db_command)

