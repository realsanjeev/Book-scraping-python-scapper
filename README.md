# Scrapy Quick Start Guide

### Setting Up a Scrapy Project

**Note:** If you're working in a global GitHub environment, it's recommended to create a virtual environment to prevent potential issues.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

1. Set up the database using Docker in detached mode. You can use the following [docker-compose.yaml](./docker-compose.yaml) configuration:

    ```bash
    docker compose up -d
    ```

Alternatively, refer to [DATABASE-CMD.md](DATABASE-CMD.md) for instructions on setting up MySQL locally instead of using Docker.

2. Run the Scrapy spiders:

    ```bash
    cd bookscrape
    scrapy crawl bookspider
    cd ../quotes_scrape
    scrapy crawl quotesspider
    ```

3. Launch the Flask app:

    ```bash
    python app.py
    ```

---

### Starting a New Scrapy Project

1. To create a new Scrapy project, use the following command:
    ```bash
    python -m scrapy startproject <projectname>
    ```

2. To run a Scrapy spider:
    ```bash
    cd <projectname>
    python -m scrapy genspider bookspider books.toscrape.com
    python -m scrapy crawl bookspider
    ```

3. To set up an interactive shell for debugging:
    ```bash
    pip install ipython
    ```

Follow these steps to quickly set up and run your Scrapy project. The provided commands will help you configure the environment, run spiders, and use the Scrapy shell for efficient debugging.
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

