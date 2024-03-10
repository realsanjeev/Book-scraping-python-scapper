'''Project uses scrappy to scrape the website and display it to user'''
import os
from flask import Flask, render_template, request
from jinja2 import Environment, PackageLoader
from pipeline import MyDatabase


app = Flask(__name__)

# Create a Jinja2 environment
env = Environment(loader=PackageLoader("app"))

# Define the custom 'enumerate' filter
def enumerate_filter(iterable, start=0):
    '''Custom filter'''
    return zip(range(start, len(iterable) + start), iterable)

env.filters['enumerate'] = enumerate_filter

# constant variable
LIMIT=10

@app.route('/')
def index():
    '''Home page view'''
    return render_template('index.html')

@app.route('/book')
def book_view():
    '''Book view from bookscrape'''
    page = request.args.get("page", 1, type=int) 
    offset = 0 if page<=1 else (page-1) * LIMIT

    database = MyDatabase(db_name="bookdb")
    tables = database.get_tables_name()
    try:
        columns = database.get_column_names(table_name=tables[0])
    except Exception:
        # Run scrapy for new clone
        os.system("python -m venv venv2")
        # chain command
        # os.system("source venv2/bin/activate && pip install --upgrade pip && cd bookscrape && scrapy crawl bookspider")
        columns = database.get_column_names(table_name=tables[0])
    
    records = database.get_records(table=tables[0], limit=LIMIT, offset=offset)
    return render_template('book.html', columns=columns, records=records)

@app.route('/quotes')
def quotes_view():
    '''Display quotes from scraping the quotes stored in db'''
    database = MyDatabase(db_name="quotesdb")
    tables = database.get_tables_name()
    columns = database.get_column_names(table_name=tables[0])
    records = database.get_records(table=tables[0])
    return render_template('quotes.html', columns=columns, records=records)

@app.route('/contacts')
def contacts_view():
    '''Contact us view'''
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
