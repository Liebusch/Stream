# sqliteTest.py
# Tests if SQLite is properly setup and creates Test.db
# expected output:
# SQLite version: <Some version number depending on what you installed>
# (1, 'Michelle')
# (2, 'Sonya')
# (3, 'Greg')
# Test.db can be deleted after test

import sqlite3 as lite
import sys

con = None

try:
    con = lite.connect('test.db')
    with con:
        cur = con.cursor()
        cur.execute('SELECT SQLITE_VERSION()')
        data = cur.fetchone()
        print("SQLite version: %s" % data)

        cur.execute("CREATE TABLE if not exists Users(Id INT, Name TEXT)")

        cur.execute("INSERT INTO Users VALUES(1,'Michelle')")
        cur.execute("INSERT INTO Users VALUES(2,'Sonya')")
        cur.execute("INSERT INTO Users VALUES(3,'Greg')")

        cur.execute("SELECT * FROM Users")

        rows = cur.fetchall()

        for row in rows:
            print(row)

except lite.Error as e:
    print("Error %s:" % e.args[0])
    sys.exit(1)
finally:
    if con:
        con.close()