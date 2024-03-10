# Scrapy Quick Start Guide

### Setting Up a Scrapy Project
**Note:** If using a global GitHub environment, create a virtual environment to avoid potential issues.
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

1. Run the Scrapy Spider
```bash
scrapy crawl bookspider
```

### Interactive Shell Setup
```bash
pip install ipython
```

### Starting a New Scrapy Project
```bash
scrapy startproject <projectname>
```

### Running a Scrapy Program
```bash
cd <projectname>
scrapy genspider bookspider books.toscrape.com
scrapy crawl bookspider
```

Follow these steps to start and run your Scrapy project efficiently. Use the provided commands to set up the environment, run the spider, and interact with the Scrapy shell for seamless web scraping.


Sample file for `bookscrape.py`
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
            next_page= 'catalogue/' + next_page if 'catalogue' not in next_page else  next_page
            next_page_url = "https://books.toscrape.com/" + next_page
            yield response.follow(next_page_url, callback=self.parse)
```
### To save scraped data in file
1. Rewrite file every time you scrapy
```bash
$ scrapy crawl bookspider -O data.csv
```
2. Append the data in same file
```bash
$ scrapy crawl bookspider -0 data.csv
```
3. You can specify the way file is scrape in `settings.py`
```python
FEEDS = {
    'book.json': {'format': 'json'}
}
```
Run scrapy as usual. It saves file in `data.json`
```bash
$ scrapy crawl bookspider
```

For database installation. See: [DATABASE-CMD.md](https://github.com/realsanjeev/Book-scraping-python-scapper/blob/main/DATABASE-CMD.md)

## Python package manager for mySql
```bash
pip install mysql-connector-python
```
Create a database and proceed. Change database name in `bookscrape/bookscrape/pipeline.py` `SaveToMySQLPipeline` to your database
## For rotating proxy
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

Feel free to modify and enhance this `README.md` as needed to match your specific project details. The provided steps are generic, and you should customize them according to the actual setup and configuration of your "Web-Scrapping-python-scrapper" project.

