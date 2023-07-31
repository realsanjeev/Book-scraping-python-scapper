import scrapy
from quotes_scrape.items import QuotesScrapeItem, AuthorScrapeItem

class QuotespiderSpider(scrapy.Spider):
    name = "quotespider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        quotes = response.css(".row .quote")
        for quote in quotes:
            relative_url = quote.css("span a::attr(href)").get()
            about_url = "https://quotes.toscrape.com" + relative_url
            quote_item = QuotesScrapeItem()

            quote_item["quote"] = quote.css(".text::text").get()
            quote_item["author"] = quote.css(".author::text").get()
            quote_item["tags"] = quote.css(".tags .tag::text").getall()
            yield response.follow(about_url,
                                    callback=self.parse_quotes,
                                    meta={"quote_data": quote_item})

        next_page = response.css(".pager .next a::attr(href)").get()
        if next_page is not None:
            next_page_url = "https://quotes.toscrape.com" + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_quotes(self, response):
        # Get quote_data from the meta attribute
        quote_data = response.meta["quote_data"]
        author_info = response.css(".author-details")

        author_data = AuthorScrapeItem()
        author_data["name"] = response.css(".author-title::text").get()
        author_data["dob"] = response.css(".author-born-date::text").get()
        author_data["birth_place"] = author_info.css(".author-born-location::text").get()
        author_data["description"] = author_info.css(".author-description::text").get()
        quote_data["author_info"] = author_data

        yield quote_data
