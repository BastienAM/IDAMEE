import sqlite3

connection = sqlite3.connect("snds_2235.db")
cursor = connection.cursor()
cursor.execute("SELECT 'a',* FROM AT_1IJ_V;")
results = cursor.fetchall()
for r in results:
    print(r)
cursor.close()
connection.close()

