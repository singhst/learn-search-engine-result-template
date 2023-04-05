import sqlite3

conn = sqlite3.connect('search_engine.db')

cur = conn.cursor()
cursor = cur.execute("SELECT version_num from alembic_version")
for row in cursor:
    print("version_num = ", row[0])
conn.close()