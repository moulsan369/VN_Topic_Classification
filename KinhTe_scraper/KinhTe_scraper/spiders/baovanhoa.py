import scrapy

class BaovanhoaSpider(scrapy.Spider):
    name = "baovanhoa"
    allowed_domains = ["baovanhoa.vn"]
    start_urls = ["https://baovanhoa.vn/kinh-te/"]

    def __init__(self, *args, **kwargs):
        super(BaovanhoaSpider, self).__init__(*args, **kwargs)
        self.url_count = 0
        self.url_limit = 710
        self.seen_urls = set()

    def parse(self, response):
        if self.url_count >= self.url_limit:
            return
        article_urls = response.css('.story__title a::attr(href)').getall()
        for url in article_urls:
            if self.url_count >= self.url_limit:
                break
            full_url = response.urljoin(url)
            if full_url not in self.seen_urls:
                self.seen_urls.add(full_url)
                self.url_count += 1
                yield {'url': full_url}
        if self.url_count < self.url_limit:
            next_page = response.css('#nextControl::attr(href)').get()
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)