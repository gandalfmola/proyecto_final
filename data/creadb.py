import sqlite3

connection = sqlite3.connect("data/registro.db")

cur = connection.cursor()

f = open("data/create.sql", "r")
query = f.read()
cur.execute(query)