from os import environ as env
from os import urandom, path
import sqlite3
import json

# Schema
db = sqlite3.connect('gixnay.db')
db_cursor = db.cursor()
db_cursor.execute("""CREATE TABLE IF NOT EXISTS Countries (
    name                    TEXT NOT NULL,
        -- name of country
    abbreviation            VARCHAR(2),
        -- two-letter abbreviation of country
    top_level_domain        TEXT,
        -- Internet TLD of country
    calling_code            INTEGER,
        -- Phone number country code
    land_area               INTEGER,
        -- Square mile land area
    population              INTEGER,
        -- Population of entire country, including military
    mil_spending            INTEGER, -- Annual budget for military spending
    mil_personnel           INTEGER,
        -- Active military personnel, not reserves
    gross_domestic_product  INTEGER,
        -- Cash value of all assets in country
        -- Can calculate GDP per capita with this and population
    permission_level        INTEGER NOT NULL,
        -- 0 - Read, 1 - Write
    password                VARCHAR(128) NOT NULL
        -- 128-byte base16 SHA512 hash
)""")
db_cursor.execute("""CREATE TABLE IF NOT EXISTS Config (
    secret_key  VARCHAR(64) NOT NULL
        -- used for signing cookies stored by web client(s)
)""")

# Check if secret key exists, and if not, generate
secret_key: str = None
for key in db_cursor.execute("""SELECT secret_key FROM Config"""):
    if secret_key is None:
        secret_key = key
    else:
        raise Exception('Field secret_key exists twice in Config')
if secret_key is None:
    print("Found no secret key, generating new one")
    secret_key = urandom(64)
    db_cursor.execute(
            """INSERT INTO Config (secret_key) VALUES (?)""",
            (secret_key,))
    db.commit()

# Get config from XDG_CONFIG_HOME/gixnaydb/conf.json
# XDG_CONFIG_HOME defaults to $HOME/.config
try:
    conf_path = env['XDG_CONFIG_HOME']
except Exception as e:
    print(f"Error using XDG_CONFIG_HOME: {type(e)}({e})")
    conf_path = path.join(env['HOME'], '.config')
    print(f"Falling back to {conf_path}")
with open(path.join(conf_path, 'gixnaydb/conf.json')) as f:
    config = json.loads(f.read())


def check_auth(auth):
    raise NotImplementedError()


# Use this to select all columns in a table, v1 compatible
# Don't use * in the event that a new schema is used
# This way, we can select only the values this API is prepared to deal with
query = """name,abbreviation,top_level_domain,calling_code,land_area,
    population,mil_spending,mil_personnel,gross_domestic_product,
    permission_level,password"""
query = query.replace('\r', '').replace('\n', '').replace(' ', '')
dz_keys_p = query.split(',')  # probably don't use this
dz_keys = [key for key in dz_keys_p if key != "password"]  # use this instead


def dz(_input):
    """Convert a Cursor.execute() result into a dict()

    :_input: Cursor.execute().fetchone() value
    :returns: dict"""
    return dict(zip(dz_keys, _input))


def get_country_names():
    """Yield a list of `name` from Countries

    :returns: generator(name, [name...])"""
    for country in db_cursor.execute(
            "SELECT name FROM Countries ORDER BY name"):
        yield country[0]


def get_countries(key="name"):
    """Yield a list of countries

    :key: Key used for ordering, 'name' by default
    :returns: generator(dz(country)[, dz(country)...])
    """
    for country in db_cursor.execute(
            f"SELECT {query} FROM Countries ORDER BY ?", (key,)):
        yield dz(country)


def get_countries_by(key, value):
    """Yield a list of countries by value

    :key: Key used for selection
    :value: Value used for selection
    :returns: dz(country)
    """
    for country in db_cursor.execute(
            f"SELECT {query} FROM Countries WHERE {key} LIKE ?", (value,)):
        yield dz(country)
