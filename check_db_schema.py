import sqlite3, json

conn = sqlite3.connect('hunger_helper.db')
c = conn.cursor()

c.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
for name, sql in c.fetchall():
    print(f"Table {name}: {sql}\n")
