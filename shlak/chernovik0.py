import sqlite3 as sl

con = sl.connect('my-test.db')

with con:
    data = con.execute("SELECT * FROM USER WHERE age <= 220")
    for row in data:
        print(row)