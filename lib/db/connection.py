import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "schema.db")

CONN = sqlite3.connect(DB_PATH)
CURSOR = CONN.cursor()