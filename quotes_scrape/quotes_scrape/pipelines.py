# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single 
from datetime import datetime
from itemadapter import ItemAdapter
from quotes_scrape.items import QuotesScrapeItem, AuthorScrapeItem
import configparser
import mysql.connector

config = configparser.ConfigParser()
config.read('config.ini')

# config variable
DB_HOST     = config["DATABASE"]["db_host"]
DB_USER     = config["DATABASE"]["db_user"]
DB_PASSWORD = config["DATABASE"]["db_password"]
DB_NAME     = config["DATABASE"]["db_name"]

class QuotesScrapePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item=item)

        ## strip all trailing and leading whitespaces from strings in value if any
        field_names = ["author", "quote"]

        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value.strip()
        
        # lowercase tags
        field_tags = "tags"
        tags = adapter.get(field_tags)
        adapter[field_tags] = [tag.lower().strip() for tag in tags]

        # cleaning author_data
        author_field = "author_info"
        author_data = adapter.get(author_field)
        for (key, values) in author_data.items():
            author_data[key] = author_data[key].strip().replace("\"", "'")
        adapter[author_field] = author_data
        return item


class SaveQuotesItemMySQL:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        self.cur = self.conn.cursor()
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER NOT NULL AUTO_INCREMENT,
            author VARCHAR(128),
            tags VARCHAR(255),
            quote TEXT,
            PRIMARY KEY (id)
        )
        """)
        self.conn.commit()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS author (
            name VARCHAR(128),
            dob DATE,
            birthplace VARCHAR(255),
            description TEXT,
            quote_id INTEGER,
            FOREIGN KEY (quote_id) REFERENCES quotes(id)
        )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        author_item = item["author_info"]

        # Parse the date and format it to 'YYYY-MM-DD'
        dob_formatted = datetime.strptime(author_item["dob"], '%B %d, %Y').strftime('%Y-%m-%d')
    
        
        # Insert data into the 'quotes' table
        self.cur.execute("""
            INSERT INTO quotes (author, tags, quote) VALUES (%s, %s, %s)
            """,
            (item["author"],
            (',').join(item["tags"]),
            item["quote"])
        )

        # Fetch the last inserted row ID (quote_id)
        quote_id = self.cur.lastrowid

        # Insert data into the 'author' table using the fetched quote_id
        self.cur.execute("""
            INSERT INTO author (name, dob, birthplace, description, quote_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (author_item["name"],
            dob_formatted,
            author_item["birth_place"],
            author_item["description"],
            quote_id) 
        )

        # Commit changes to the database
        self.conn.commit()
        return item
    
    def close_spider(self, spider):
        # Close cursor and connection to the database.
        self.cur.close()
        self.conn.close()

