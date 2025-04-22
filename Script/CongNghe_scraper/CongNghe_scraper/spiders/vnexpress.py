import scrapy

class VnexpressSpider(scrapy.Spider):
    name = "vnexpress"
    allowed_domains = ["vnexpress.net"]
    start_urls = ["https://vnexpress.net/cong-nghe"]

    def __init__(self, *args, **kwargs):
        super(VnexpressSpider, self).__init__(*args, **kwargs)
        self.url_count = 0
        self.url_limit = 1000
        self.seen_urls = set()
        self.current_page = 1
        self.max_pages = 50

    def parse(self, response):
        if self.url_count >= self.url_limit:
            return

        # Trang 1: Dùng selector 'h3.title-news a'
        if self.current_page == 1:
            article_urls = response.css('h3.title-news a::attr(href)').getall()
        # Trang 2 trở đi: Dùng selector 'h2.title-news a'
        else:
            article_urls = response.css('h2.title-news a::attr(href)').getall()

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
            next_page_url = f"https://vnexpress.net/cong-nghe-p{self.current_page}"
            yield scrapy.Request(next_page_url, callback=self.parse)