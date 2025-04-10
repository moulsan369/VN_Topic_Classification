import scrapy

class DaibieunhandanSpider(scrapy.Spider):
    name = "daibieunhandan"
    allowed_domains = ["daibieunhandan.vn"]
    start_urls = ["https://daibieunhandan.vn/chinh-tri/"]

    def __init__(self, *args, **kwargs):
        super(DaibieunhandanSpider, self).__init__(*args, **kwargs)
        self.url_count = 0
        self.url_limit = 1000
        self.seen_urls = set()
        self.current_page = 0

    def parse(self, response):
        if self.url_count >= self.url_limit:
            return

        article_urls = response.css('.story__heading a::attr(href)').getall()
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
            next_page = f"https://daibieunhandan.vn/chinh-tri/pagina{self.current_page}"
            yield scrapy.Request(next_page, callback=self.parse)