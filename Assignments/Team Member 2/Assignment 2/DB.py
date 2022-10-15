import sqlite3 as sql

con=sql.connect("database.db")
print("successfully connect")
con.execute("create table register(name text,email text,password text)")
print("table create successfully")
con.close()