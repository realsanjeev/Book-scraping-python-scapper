## Middleware in Scrapy
Middleware in Scrapy is a crucial component that plays a significant role in the web scraping framework's request/response processing pipeline. It acts as a series of hooks or processing units through which each request and response passes, allowing you to intercept, modify, or handle them at various stages of the crawling process. Middleware enables you to add custom functionality to Scrapy, such as user-agent rotation, proxy handling, request filtering, and more.

Scrapy's middleware works with both outbound requests (sent to websites for scraping) and inbound responses (received from websites after scraping). The middleware pipeline is a chain of Python classes, and each class can implement specific functionalities before and after a request is sent or a response is received.

The middleware components in Scrapy are organized into two categories: `Spider Middleware` and `Downloader Middleware`.

1. Spider Middleware:
   Spider Middleware operates between the Scrapy engine and the spider. It provides hooks that allow you to modify spider input (requests) and output (items and scraped data) before they reach the spider or after they leave it. Common use cases for spider middleware include adding custom headers to requests, filtering URLs, and handling cookies.

2. Downloader Middleware:
   Downloader Middleware operates between the Scrapy engine and the downloader (responsible for handling HTTP requests). It provides hooks to intercept and modify requests before they are sent to the target website and responses before they are processed by the spiders. Common use cases for downloader middleware include handling proxies, managing user-agents, and managing cookies.

### Python package for 
```
pip install scrapeops-scrapy-proxy-sdk
```


from urllib.parse import urlencode
import scrapy
from bookscrape2.items import BookItem

def get_proxy_url(url):
    API_KEY = "5cdf4d71-9fef-493b-93c8-3e0e160a4c06"
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com", "proxy.scrapeops.io"]
    start_urls = ["https://books.toscrape.com"]

    def start_requests(self):
        yield scrapy.Request(url=get_proxy_url(self.start_urls[0]), callback=self.parse)

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()
            if 'catalogue/' in relative_url:
                book_url = "https://books.toscrape.com/" + relative_url
            else:
                book_url = "https://books.toscrape.com/catalogue/" + relative_url
            yield response.follow(book_url, callback=self.parse_book_details)

        next_page = response.css('.pager li.next a::attr("href")').get()
        if next_page is not None:
            next_page= 'catalogue/' + next_page if 'catalogue' not in next_page else  next_page
            next_page_url = "https://books.toscrape.com/" + next_page
            yield response.follow(get_proxy_url(url=next_page_url), callback=self.parse)

    def parse_book_details(self, response):
        book_detail = response.css('.page_inner')
        table_rows = response.css('table tr')
        book_item = BookItem()

        book_item['url'] = response.url
        book_item['name'] = book_detail.css('.product_main h1::text').get()
        book_item['price_excl_tax'] = table_rows[2].css('td::text').get()
        book_item['price_incl_tax'] = table_rows[3].css('td::text').get()
        book_item['tax'] = table_rows[4].css('td::text').get()
        book_item['price'] = book_detail.css('.product_main .price_color::text').get()
        book_item['type'] = table_rows[1].css('td::text').get()
        book_item['genre'] = response.xpath('//*[@id="default"]/div/div/ul/li[3]/a/text()').get()
        book_item['availability'] = table_rows[5].css('td::text').get()
        book_item['no_of_reviews'] = table_rows[6].css('td::text').get()
        book_item['stars'] = book_detail.css('.product_main .star-rating').attrib['class'].split()[1]
        book_item['description'] = response.xpath('//*[@id="content_inner"]/article/p/text()').get()

        yield book_item


