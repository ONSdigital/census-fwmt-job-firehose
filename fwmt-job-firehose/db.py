from flask import g, current_app
from flask.cli import with_appcontext
import sqlite3
import click
import json
import uuid

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)
    app.cli.add_command(load_address_json)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect_db():
    conn = sqlite3.connect(current_app.instance_path + '/firehose.db')
    conn.row_factory = dict_factory
    return conn

def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

def close_db(e = None):
    db = g.pop('db', None)
    if db is not None:
        db.commit()
        db.close()

@click.command('init-db')
@with_appcontext
def init_db():
    """Set up the initial database tables"""
    get_db().cursor().execute('''CREATE TABLE IF NOT EXISTS ids (id TEXT PRIMARY KEY, time TEXT DEFAULT CURRENT_TIMESTAMP)''')
    get_db().cursor().execute(
        '''CREATE TABLE IF NOT EXISTS addresses (
          sampleUnitRef TEXT, type TEXT, estabType TEXT, locality TEXT, organisationName TEXT, category TEXT,
          line1 TEXT, line2 TEXT, line3 TEXT, line4 TEXT, townName TEXT, postcode TEXT, country TEXT,
          ladCode TEXT, latitude TEXT, longitude TEXT
        )''')

@click.command('load-address-json')
@click.argument('filename')
@with_appcontext
def load_address_json(filename):
    """This loads addresses from a JSON file into the database. The JSON file should contain the following:

    \b
    A name at $.name
    A longer description at $.longname
    An array of addresses at $.addresses

    \b
    Each address can contain the following:
      $.sampleUnitRef, $.type, $.estabType, $.locality, $.organisationName, $.category, $.line1, $.line2, $.line3, $.line4, $.townName, $.postcode, $.country, $.ladCode, $.latitude, $.longitude
    """

    with open(filename) as text:
        j = json.load(text)
        addresses = j['addresses']
        for address in addresses:
            get_db().cursor().execute(
                '''INSERT INTO addresses (
                sampleUnitRef, type, estabType, locality, organisationName, category,
                line1, line2, line3, line4, townName, postcode, country, ladCode, latitude, longitude
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (address.get('sampleUnitRef', None),
                 address.get('type', None),
                 address.get('estabType', None),
                 address.get('locality', None),
                 address.get('organisationName', None),
                 address.get('category', None),
                 address.get('line1', None),
                 address.get('line2', None),
                 address.get('line3', None),
                 address.get('line4', None),
                 address.get('townName', None),
                 address.get('postcode', None),
                 address.get('country', None),
                 address.get('ladCode', None),
                 address.get('latitude', '0'),
                 address.get('longitude', '0'))
            )

def generate_id():
    id = str(uuid.uuid4())
    get_db().cursor().execute('''INSERT INTO ids (id) VALUES (?)''', (id,))
    return id

# def load_addresses():
#     addresses = []
#     files = app.config['ADDRESS_FILES'].split(';')
#     for f in files:
#         with open(f) as text:
#             j = json.load(text)
#             addresses.extend(j['addresses'])
#     return addresses

# def get_addresses():
#     global addresses
#     if addresses == None:
#         addresses = load_addresses()
#     return addresses

def pick_address():
    cur = get_db().cursor()
    cur.execute('''SELECT * FROM addresses ORDER BY RANDOM() LIMIT 1''')
    return cur.fetchone()
