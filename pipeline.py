import os
import mysql.connector

class MyDatabase:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bookdb"
        )
        self.cur = self.conn.cursor()
        a = self.cur.execute("SELECT * from books limit ")
        print(a)
        print(self.conn)

if __name__ == "__main__":
    MyDatabase()