import os
import sqlite3


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATABASE_DIR = os.path.join(ROOT_DIR, "database")
DEFAULT_DATABASE_PATH = os.path.join(DATABASE_DIR, "students.db")
SCHEMA_FILE = os.path.join(ROOT_DIR, "database", "schema.sql")


def ensure_database_folder(database_path=None):
    """Create the database folder if it does not exist."""
    target = database_path or DEFAULT_DATABASE_PATH
    if target.startswith("file:"):
        return target

    directory = os.path.dirname(target)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    return target


def initialize_database(database_path=None):
    """Create the SQLite database and all required tables."""
    target = ensure_database_folder(database_path)
    is_uri_database = target.startswith("file:")
    connection = sqlite3.connect(target, uri=is_uri_database)
    connection.execute("PRAGMA foreign_keys = ON")

    with open(SCHEMA_FILE, "r", encoding="utf-8") as schema_file:
        schema_sql = schema_file.read()

    connection.executescript(schema_sql)
    connection.commit()
    connection.close()
    return target


def load_schema_sql():
    """Read the schema SQL file so it can be applied to new connections."""
    with open(SCHEMA_FILE, "r", encoding="utf-8") as schema_file:
        return schema_file.read()
