import sqlite3
import click
from flask import g
from flask.cli import with_appcontext

def connect_db():
    return sqlite3.connect('firehose_ids.db')

def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.cli.add_command
@click.command('init-db')
@with_appcontext
def init_db():
    get_db().cursor().execute('''CREATE TABLE IF NOT EXISTS ids (id TEXT PRIMARY KEY, time TEXT DEFAULT CURRENT_TIMESTAMP)''')

@app.teardown_appcontext
def close_db(e = None):
    db = g.pop('db', None)
    if db is not None:
        db.commit()
        db.close()
