import sqlite3
import os

# Paths to the schema.sql and the database file
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # from scripts/ up to project root
SCHEMA_PATH = os.path.join(BASE_DIR, 'lib', 'db', 'schema.sql')
DB_PATH = os.path.join(BASE_DIR, 'lib', 'db', 'schema.db')

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Read the schema.sql content
with open(SCHEMA_PATH, 'r') as f:
    schema_sql = f.read()

# Execute all SQL commands in schema.sql to create tables
cursor.executescript(schema_sql)

conn.commit()
conn.close()

print("Database setup complete.")
