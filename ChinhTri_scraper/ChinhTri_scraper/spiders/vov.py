import scrapy

class VovSpider(scrapy.Spider):
    name = "vov"
    allowed_domains = ["vov.vn"]
    start_urls = ["https://vov.vn/chinh-tri"]

    def __init__(self, *args, **kwargs):
        super(VovSpider, self).__init__(*args, **kwargs)
        self.url_count = 0
        self.url_limit = 1000
        self.seen_urls = set()  

    def parse(self, response):
        if self.url_count >= self.url_limit:
            return
        
        article_urls = response.css('.vovvn-title::attr(href)').getall()
        for url in article_urls:
            if self.url_count >= self.url_limit:
                break
            full_url = response.urljoin(url)
            # Kiểm tra trùng lặp
            if full_url not in self.seen_urls:
                self.seen_urls.add(full_url)
                self.url_count += 1
                yield {'url': full_url}
        if self.url_count < self.url_limit:
            next_page = response.css('a[rel="next"]::attr(href)').get()  # Phân trang
            if next_page:
                yield scrapy.Request(response.urljoin(next_page), callback=self.parse)