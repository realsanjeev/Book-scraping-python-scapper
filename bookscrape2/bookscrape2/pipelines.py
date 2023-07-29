# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#
# useful for handling different item types with a single interface
import os
from itemadapter import ItemAdapter
import mysql.connector

class Bookscrape2Pipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item=item)

        # strip all trailing and leading whitespaces from strings in value if any
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value.strip()
        
        # convert value of genre and type to lowercase
        lowercase_keys = ['genre', 'type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # get availability in number of stock
        availability_key = 'availability'
        split_string_array = adapter.get(availability_key).split("(")
        if (len(split_string_array) < 2):
            adapter[availability_key] = int(0)
        else:
            adapter[availability_key] = int(split_string_array[1].split()[0])
        
        
        # price(str) --> convert to float
        price_keys = ['price', 'price_incl_tax', 'price_excl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        # no_of_reviews(str) --> int
        reviews_key = 'no_of_reviews'
        value = adapter.get(reviews_key)
        adapter[reviews_key] = int(value)

        # change stars into equivalent int
        stars_key = 'stars'
        star_ratings = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
        value = adapter.get(stars_key, "").lower()
        adapter[stars_key] = star_ratings.get(value, 0)

        return item


class SaveToMySQLPipeline:

    def __init__(self) -> None:
        if 'CODESPACE_NAME' in os.environ:
            codespace_name = os.getenv("CODESPACE_NAME")
            codespace_domain = os.getenv("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN")
            self.CSRF_TRUSTED_ORIGINS = f'https://{codespace_name}-3306.{codespace_domain}'
        else:
            self.CSRF_TRUSTED_ORIGINS = 'localhost'
        
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='bookdb'
        )

        # Create a cursor, used to execute commands
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER NOT NULL AUTO_INCREMENT,
                url varchar(255),
                name varchar(128),
                price_excl_tax DECIMAL,
                price_incl_tax DECIMAL,
                tax DECIMAL,
                price DECIMAL,
                type varchar(32),
                genre varchar(32),
                availability integer,
                no_of_reviews integer,
                stars integer,
                description text,
                PRIMARY KEY(id)
            )
        """)
        self.conn.commit()

    def process_item(self, item, spider):
        self.cur.execute("""
        INSERT INTO books (
            url, name, price_excl_tax, price_incl_tax, tax, price,
            type, genre, availability, no_of_reviews, stars, description
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """,
    (
        item["url"],
        item["name"],
        item["price_excl_tax"],
        item["price_incl_tax"],
        item["tax"],
        item["price"],
        item["type"],
        item["genre"],
        item["availability"],
        item["no_of_reviews"],
        item["stars"],
        str(item["description"])
    ))
        self.conn.commit()
        # returning item is important in process_item method in pipeline
        return item

    def close_spider(self, spider):
        # Close cursor and connection to the database.
        self.cur.close()
        self.conn.close()
