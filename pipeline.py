'''Module to connect to mysql database'''
import os
import configparser
import mysql.connector

config = configparser.ConfigParser()
config.read('config.ini')

# config variable
DB_HOST     = config["DATABASE"]["db_host"]
DB_USER     = config["DATABASE"]["db_user"]
DB_PASSWORD = config["DATABASE"]["db_password"]
DB_NAME     = config["DATABASE"]["db_name"]


class MyDatabase:
    def __init__(self, db_host: str="localhost", 
                    db_user: str="root", 
                    db_password: str="", 
                    db_name: str="bookdb"):
        try:
            os.system("sudo service mysql start")
            self.conn = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            )
            self.cur = self.conn.cursor()
            self.db_name = db_name
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER NOT NULL AUTO_INCREMENT,
                    url VARCHAR(255),
                    upc VARCHAR(64) UNIQUE,
                    name VARCHAR(128),
                    price_excl_tax DECIMAL(10, 2),
                    price_incl_tax DECIMAL(10, 2),
                    tax DECIMAL(10, 2),
                    price DECIMAL(10, 2),
                    type VARCHAR(32),
                    genre VARCHAR(32),
                    availability INTEGER,
                    no_of_reviews INTEGER,
                    stars INTEGER,
                    description TEXT,
                    PRIMARY KEY(id)
                )
            """)
        except mysql.connector.Error as err:
            print(f"[ERROR] Cannot connect to database: {err}")
            raise Exception(f"Cannot connect to database: {err}")
        self.sys_table = ['information_schema', 'mysql', 'performance_schema', 'sys']

    def get_tables_name(self):
        self.cur.execute("SHOW TABLES;")
        all_user_tables = [table[0] for table in self.cur.fetchall() if table[0] not in self.sys_table]
        if not all_user_tables:
            if self.db_name == "bookdb":
                os.system("cd bookscrape && scrapy crawl bookspider")
            elif self.db_name == "quotesdb":
                os.system("cd quotes_scrape && scrapy crawl quotespider")
        return all_user_tables

    def get_column_names(self, table_name):
        '''Get all column names of a table'''
        self.cur.execute(f"SHOW COLUMNS FROM {table_name}")
        columns = [column[0] for column in self.cur.fetchall()]
        print(f"[INFO] Columns are: {columns}")
        return columns

    def get_records(self, table, limit=5, offset=None):
        try:
            if offset is None:
                self.cur.execute(f"SELECT * FROM {table} LIMIT {limit}")
            else:
                self.cur.execute(f"SELECT * FROM {table} LIMIT {limit} OFFSET {offset}")
            records = self.cur.fetchall()
            return records
        except mysql.connector.Error as err:
            print(f"Error occurred while reading from database: {err}")
            return f"Error occurred while reading from database: {err}"

    def close_connection(self):
        self.cur.close()
        self.conn.close()



if __name__ == "__main__":
    db = MyDatabase(db_host=DB_HOST, db_user=DB_USER, db_password=DB_PASSWORD)
    SAMPLE_TABLE_NAME = "books"
    column_names = db.get_column_names(SAMPLE_TABLE_NAME)
    all_tables = db.get_tables_name()
    db.get_records(SAMPLE_TABLE_NAME)
    # print(f"Column names of the table '{all_tables}':")
    db.close_connection()
