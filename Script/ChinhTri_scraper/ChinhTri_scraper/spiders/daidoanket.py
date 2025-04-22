import scrapy

class DaidoanketSpider(scrapy.Spider):
    name = "daidoanket"
    allowed_domains = ["daidoanket.vn"]
    start_urls = ["https://daidoanket.vn/chinh-tri"]

    def __init__(self, *args, **kwargs):
        super(DaidoanketSpider, self).__init__(*args, **kwargs)
        self.url_count = 0
        self.url_limit = 1000
        self.seen_urls = set()

    def parse(self, response):
        if self.url_count >= self.url_limit:
            return
        article_urls = response.css('.b-grid__title a::attr(href)').getall()
        for url in article_urls:
            if self.url_count >= self.url_limit:
                break
            full_url = response.urljoin(url)
            if full_url not in self.seen_urls:
                self.seen_urls.add(full_url)
                self.url_count += 1
                yield {'url': full_url}
        if self.url_count < self.url_limit:
            next_page = response.css('.c-more a::attr(href)').get()
            if next_page and next_page != 'javascript:;':
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)