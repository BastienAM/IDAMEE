import sqlite3
import ClassModel


conn = sqlite3.connect("../database/snds_2235.db")

qry = open('./SQL/query_hospital.sql', 'r').read()
print(qry)

cursor = conn.cursor()
cursor.execute(qry)


row = cursor.fetchone()
while row != None:
    print(row)
    row = cursor.fetchone()
cursor.close()

# On ferme la connection à la base de donnée
conn.close()