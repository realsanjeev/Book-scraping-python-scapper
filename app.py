from flask import Flask, render_template
from pipeline import MyDatabase
from jinja2 import Environment, PackageLoader

app = Flask(__name__)

# Create a Jinja2 environment
env = Environment(loader=PackageLoader("app"))

# Define the custom 'enumerate' filter
def enumerate_filter(iterable, start=0):
    return zip(range(start, len(iterable) + start), iterable)

env.filters['enumerate'] = enumerate_filter



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book')
def book_view():
    database = MyDatabase(db_name="bookdb")
    tables = database.get_tables_name()
    columns = database.get_column_names(table_name=tables[0])
    records = database.get_records(table=tables[0])
    return render_template('book.html', columns=columns, records=records)

@app.route('/quotes')
def quotes_view():
    database = MyDatabase(db_name="quotesdb")
    tables = database.get_tables_name()
    columns = database.get_column_names(table_name=tables[0])
    records = database.get_records(table=tables[0])
    return render_template('quotes.html', columns=columns, records=records)

@app.route('/contacts')
def contacts_view():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
