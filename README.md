# Scrapy Quick Start Guide

### Setting Up a Scrapy Project

**Note:** If you are using a global GitHub environment, create a virtual environment to avoid potential issues.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

1. Set up the database using [DATABASE-CMD.md](DATABASE-CMD.md).

2. Run the Scrapy Spider:

    ```bash
    cd bookscrape
    scrapy crawl bookspider
    cd ../quotes_scrape
    scrapy crawl quotesspider
    ```

3. Run the Flask app:

    ```bash
    python app.py
    ```

### Interactive Shell Setup

To set up an interactive shell:

```bash
pip install ipython
```

### Starting a New Scrapy Project

To start a new Scrapy project:

```bash
scrapy startproject <projectname>
```

### Running a Scrapy Program

To run a Scrapy program:

```bash
cd <projectname>
scrapy genspider bookspider books.toscrape.com
scrapy crawl bookspider
```

Follow these steps to start and run your Scrapy project efficiently. Use the provided commands to set up the environment, run the spider, and interact with the Scrapy shell for seamless web scraping.

### Sample File for `bookscrape.py`

```python
import scrapy

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('.product_pod')
        for book in books:
            yield {
                'name': book.css('h3 a::text').get(),
                'price': book.css('.product_price .price_color::text').get(),
                'url': book.css('h3 a').attrib['href']
            }
        
        next_page = response.css('.pager li.next a::attr("href")').get()
        if next_page is not None:
            next_page = 'catalogue/' + next_page if 'catalogue' not in next_page else next_page
            next_page_url = "https://books.toscrape.com/" + next_page
            yield response.follow(next_page_url, callback=self.parse)
```

### Saving Scraped Data to a File

1. To overwrite the file every time you run Scrapy:

    ```bash
    scrapy crawl bookspider -O data.csv
    ```

2. To append data to the same file:

    ```bash
    scrapy crawl bookspider -o data.csv
    ```

3. You can specify the format for saving the file in `settings.py`:

    ```python
    FEEDS = {
        'book.json': {'format': 'json'}
    }
    ```

    Run Scrapy as usual. It will save the file as `book.json`.

    ```bash
    scrapy crawl bookspider
    ```

For database installation, see: [DATABASE-CMD.md](https://github.com/realsanjeev/Book-scraping-python-scapper/blob/main/DATABASE-CMD.md)

### Python Package Manager for MySQL

To install the MySQL connector for Python:

```bash
pip install mysql-connector-python
```

Create a database and update the database name in `bookscrape/bookscrape/pipeline.py` under the `SaveToMySQLPipeline` class to match your database.

### For Rotating Proxies

To install the rotating proxies middleware for Scrapy:

```bash
pip install scrapy-rotating-proxies
```
<!-- ##### For config env variable -->




## Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to submit a pull request.

## Contact Me

<table>
  <tr>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/instagram.png" alt="Instagram" width="50" height="50"></td>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/twitter.png" alt="Twitter" width="50" height="50"></td>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/github.png" alt="GitHub" width="50" height="50"></td>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/linkedin-logo.png" alt="LinkedIn" width="50" height="50"></td>
  </tr>
</table>

## License

This project is licensed under the [GNU GENERAL PUBLIC LICENSE](LICENSE).

---


This guide provides the steps to set up and run a Scrapy project, including running spiders, managing the environment, and handling data output. Use it to streamline your web scraping tasks.

Feel free to modify and enhance this `README.md` as needed to match your specific project details. The provided steps are generic, and you should customize them according to the actual setup and configuration of your "Web-Scrapping-python-scrapper" project.

