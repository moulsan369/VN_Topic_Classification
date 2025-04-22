import scrapy

class VietnamnetSpider(scrapy.Spider):
    name = "vietnamnet"
    allowed_domains = ["vietnamnet.vn"]
    start_urls = ["https://vietnamnet.vn/thong-tin-truyen-thong/cong-nghe"]

    def __init__(self, *args, **kwargs):
        super(VietnamnetSpider, self).__init__(*args, **kwargs)
        self.url_count = 0
        self.url_limit = 300
        self.seen_urls = set()
        self.current_page = 0
        self.max_pages = 50

    def parse(self, response):
        if self.url_count >= self.url_limit:
            return

        article_urls = response.css('h3.horizontalPost__main-title a::attr(href)').getall()
        for url in article_urls:
            if self.url_count >= self.url_limit:
                break
            full_url = response.urljoin(url)
            if full_url not in self.seen_urls:
                self.seen_urls.add(full_url)
                self.url_count += 1
                yield {'url': full_url}

        if self.url_count < self.url_limit and self.current_page < self.max_pages:
            self.current_page += 1
            next_page_url = f"https://vietnamnet.vn/thong-tin-truyen-thong/cong-nghe-page{self.current_page}"
            yield scrapy.Request(next_page_url, callback=self.parse)