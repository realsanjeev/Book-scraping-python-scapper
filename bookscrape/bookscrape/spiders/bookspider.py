import scrapy
from bookscrape.items import BookItem

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

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
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_details(self, response):
        book_detail = response.css('.page_inner')
        table_rows = response.css('table tr')
        book_item = BookItem()

        book_item['url'] = response.url
        book_item['upc'] = table_rows[0].css('td::text').get()
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
