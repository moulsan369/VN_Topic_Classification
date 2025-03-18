import scrapy


class BaochinhphuSpider(scrapy.Spider):
    name = "baochinhphu"
    allowed_domains = ["baochinhphu.vn"]
    start_urls = ["https://baochinhphu.vn"]

    def parse(self, response):
        pass
