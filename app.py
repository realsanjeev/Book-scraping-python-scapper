from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book')
def book_view():
    return render_template('book.html')

@app.route('/quotes')
def quotes_view():
    return render_template('quotes.html')

@app.route('/contacts')
def contacts_view():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
