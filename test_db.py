import sqlite3
import os

print("Current folder:", os.getcwd())

conn = sqlite3.connect("students.db")
conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER)")
conn.commit()
conn.close()

print("Database created successfully")
