import scrapy

class ThanhnienSpider(scrapy.Spider):
    name = "thanhnien"
    allowed_domains = ["thanhnien.vn"]
    start_urls = ["https://thanhnien.vn/cong-nghe.htm"]

    def __init__(self, *args, **kwargs):
        super(ThanhnienSpider, self).__init__(*args, **kwargs)
        self.url_count = 0
        self.url_limit = 1000
        self.seen_urls = set()

    def parse(self, response):
        if self.url_count >= self.url_limit:
            return
        article_urls = response.css('h3 a::attr(href)').getall()
        for url in article_urls:
            if self.url_count >= self.url_limit:
                break
            full_url = response.urljoin(url)
            self.url_count += 1
            yield {'url': full_url}
        if self.url_count < self.url_limit:
            next_page = response.css('a.next::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, self.parse)