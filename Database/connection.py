# connection.py
# Class to create a new database connection

import sqlite3 as lite

class Connection:
    # connection object
    con = None
    # cursor object
    cur = None

    def __init__(self, dbName):
        try:
            self.con = lite.connect("file:Database/" + dbName + "?mode=rw", uri=True)
        except lite.OperationalError as e:
            print(e)
        self.cur = self.con.cursor()
