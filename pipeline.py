'''Module to connect to mysql database'''
import os
import configparser
import mysql.connector

config = configparser.ConfigParser()
config.read('config.ini')

# config variable
db_host = config["DATABASE"]["host"]
db_user = config["DATABASE"]["user"]
db_password = config["DATABASE"]["password"]

class MyDatabase:
    def __init__(self, db_name="bookdb"):
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
        except mysql.connector.Error as err:
            raise f"Cannot connect to database: {err}"
        self.sys_table = ['information_schema', 'mysql', 'performance_schema', 'sys']

    def get_tables_name(self):
        self.cur.execute("SHOW TABLES;")
        all_user_tables = [table[0] for table in self.cur.fetchall() \
                           if table[0] not in self.sys_table]
        if not all_user_tables:
            if self.db_name=="bookdb":
                # must be chained to execute
                os.system("cd bookscrape && scrapy crawl bookspider")
            if self.db_name=="quotesdb":
                os.system("cd quotes_scrape && scrapy crawl quotespider")
        return all_user_tables

    def get_column_names(self, table_name):
        '''Get all column name of table'''
        self.cur.execute(f"SHOW COLUMNS FROM {table_name}")
        # return info of table columns
        columns = [column[0] for column in self.cur.fetchall()]
        print('*'*43, columns)
        return columns

    def get_records(self, table, limit=5, offset=None):
        try:
            if offset is None:
                self.cur.execute(f"SELECT * FROM {table} LIMIT {limit}")
            else:
                self.cur.execute(f"SELECT * FROM {table} LIMIT {limit} OFFSET {offset}")
            records = self.cur.fetchall()
            return records
        except mysql.connector.errors.Error as err:
            print(err)
            return f"Error occurred while reading Database: {err}"


    def close_connection(self):
        self.cur.close()
        self.conn.close()


if __name__ == "__main__":
    db = MyDatabase()
    SAMPLE_TABLE_NAME = "books"
    column_names = db.get_column_names(SAMPLE_TABLE_NAME)
    all_tables = db.get_tables_name()
    db.get_records(SAMPLE_TABLE_NAME)
    # print(f"Column names of the table '{all_tables}':")
    db.close_connection()
