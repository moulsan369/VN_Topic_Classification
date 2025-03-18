import scrapy

class ThoibaonganhangSpider(scrapy.Spider):
    name = "thoibaonganhang"
    allowed_domains = ["thoibaonganhang.vn"]
    start_urls = ["https://thoibaonganhang.vn/chinh-tri"]

    def __init__(self, *args, **kwargs):
        super(ThoibaonganhangSpider, self).__init__(*args, **kwargs)
        self.url_count = 0
        self.url_limit = 1000
        self.seen_urls = set()  # Để tránh trùng lặp

    def parse(self, response):
        if self.url_count >= self.url_limit:
            return
        article_urls = response.css('.article-title a::attr(href)').getall()  # URL bài viết
        for url in article_urls:
            if self.url_count >= self.url_limit:
                break
            full_url = response.urljoin(url)
            if full_url not in self.seen_urls:
                self.seen_urls.add(full_url)
                self.url_count += 1
                yield {'url': full_url}
        if self.url_count < self.url_limit:
            next_page = response.css('.__MB_NEXT_URL::attr(value)').get()  # Phân trang
            if next_page:
                yield scrapy.Request(next_page, callback=self.parse)