import scrapy


class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        quotes = response.css(".row .quote")
        for quote in quotes:
            yield {
                "quote": quote.css(".text::text").get(),
                "author": quote.css(".author::text").get(),
                "tags": quote.css(".tags .tag::text").getall()
            }

        next_page = response.css(".pager .next a::attr(href)").get()
        if next_page is not None:
            next_page_url = "https://quotes.toscrape.com" + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_quotes(self, response):
        pass
