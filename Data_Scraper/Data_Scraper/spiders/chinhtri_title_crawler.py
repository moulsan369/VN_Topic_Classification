import scrapy
import json

class ChinhTriTitleCrawlerSpider(scrapy.Spider):
    name = "chinhtri_title_crawler"
    allowed_domains = ["vov.vn"]

    custom_settings = {
        'FEEDS': {
            'chinhtri_titles.json': {
                'format': 'json',
                'overwrite': False,
                'fields': ['title', 'label'],
                'encoding': 'utf-8',
            }
        }
    }

    def start_requests(self):
        try:
            with open('E:\CDTN\Convert_file\ChinhTri_urls_1000.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            urls = [item['url'] for item in data if 'url' in item]
            
            for url in urls:
                if url.startswith('http://') or url.startswith('https://'):
                    yield scrapy.Request(url, callback=self.parse)
                else:
                    self.logger.warning(f"Invalid URL skipped: {url}")
        except FileNotFoundError:
            self.logger.error("File 'ChinhTri_urls_1000.json' not found in project directory")
        except json.JSONDecodeError:
            self.logger.error("Invalid JSON format in 'ChinhTri_urls_1000.json'")

    def parse(self, response):
        # Lấy văn bản trong thẻ <title>
        title = response.xpath('//title/text()').get()
        yield {
            'title': title.strip() if title else '',
            'label': 'Chính trị'
        }