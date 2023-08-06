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
            raise (f"Cannot connect to database: {err}")
        self.sys_table = ['information_schema', 'mysql', 'performance_schema', 'sys']

    def get_tables_name(self):
        self.cur.execute(f"SHOW TABLES;")
        all_user_tables = [table[0].decode('utf-8') for table in self.cur.fetchall() \
                           if table[0] not in self.sys_table]
        if not len(all_user_tables):
            if self.db_name=="bookdb":
                os.system("cd bookscrape")
                os.system("scrapy crawl bookspider")
            if self.db_name=="quotesdb":
                os.system("cd quotes_scrape")
                os.system("scrapy crawl quotespider")
        return all_user_tables

    def get_column_names(self, table_name):
        self.cur.execute(f"SHOW COLUMNS FROM {table_name}")
        # return info of table columns
        columns = [column[0] for column in self.cur.fetchall()]
        return columns
    
    def get_records(self, table, limit=None):
        try:
            if limit is None:
                self.cur.execute(f"""SELECT * FROM {table}""")
            else:
                self.cur.execute(f"""SELECT * FROM {table} LIMIT {limit}""")
            records = self.cur.fetchall()
            return records
        except mysql.connector.errors.Error as err:
            print(err)
            return f"Error Occured while reading Database: {err}"

    def close_connection(self):
        self.cur.close()
        self.conn.close()


if __name__ == "__main__":
    db = MyDatabase()
    sample_table_name = "books"
    column_names = db.get_column_names(sample_table_name)
    all_tables = db.get_tables_name()
    db.get_records(sample_table_name)
    # print(f"Column names of the table '{all_tables}':")
    db.close_connection()
