import scrapy

class ConglySpider(scrapy.Spider):
    name = "congly"
    allowed_domains = ["congly.vn"]
    start_urls = ["https://congly.vn/chinh-tri"]

    def __init__(self, *args, **kwargs):
        super(ConglySpider, self).__init__(*args, **kwargs)
        self.url_count = 0
        self.url_limit = 100
        self.seen_urls = set()
        self.current_page = 0

    def parse(self, response):
        if self.url_count >= self.url_limit:
            return

        article_urls = response.css('.b-grid__img a::attr(href)').getall()
        for url in article_urls:
            if self.url_count >= self.url_limit:
                break
            full_url = response.urljoin(url)
            if full_url not in self.seen_urls:
                self.seen_urls.add(full_url)
                self.url_count += 1
                yield {'url': full_url}

        if self.url_count < self.url_limit:
            self.current_page += 1
            next_page = f"https://congly.vn/chinh-tri/trang-{self.current_page}.html"
            yield scrapy.Request(next_page, callback=self.parse)