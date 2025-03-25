import scrapy

class VtvSpider(scrapy.Spider):
    name = "vtv"
    allowed_domains = ["vtv.vn"]
    start_urls = ["https://vtv.vn/chinh-tri.htm"]

    def __init__(self, *args, **kwargs):
        super(VtvSpider, self).__init__(*args, **kwargs)
        self.url_count = 0
        self.url_limit = 1000
        self.seen_urls = set()
        self.current_page = 1

    def parse(self, response):
        if self.url_count >= self.url_limit:
            return

        article_urls = response.css('.focus_left h2 a::attr(href)').getall()
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
            # Thử các định dạng URL phân trang
            possible_next_pages = [
                f"https://vtv.vn/chinh-tri/trang/{self.current_page}.htm",
                f"https://vtv.vn/chinh-tri/page/{self.current_page}",
                f"https://vtv.vn/chinh-tri.htm?page={self.current_page}"
            ]
            for next_page in possible_next_pages:
                yield scrapy.Request(next_page, callback=self.parse, errback=self.handle_error)

    def handle_error(self, failure):
        # Bỏ qua lỗi 404 hoặc các lỗi khác
        pass