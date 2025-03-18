# Scrapy settings for ChinhTri_scraper project

BOT_NAME = "ChinhTri_scraper"

SPIDER_MODULES = ["ChinhTri_scraper.spiders"]
NEWSPIDER_MODULE = "ChinhTri_scraper.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "ChinhTri_scraper (+http://www.yourdomain.com)"  # Có thể tùy chỉnh

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 5  # Chờ 5 giây giữa các request

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16  # Giữ mặc định hoặc tăng nếu cần

# Giới hạn độ sâu phân trang
DEPTH_LIMIT = 10

# Cấu hình lưu file JSON
FEEDS = {
    'politics_urls.json': {
        'format': 'json',
        'overwrite': False,  # Không ghi đè, thêm dữ liệu vào file hiện có
        'fields': ['url'],   # Chỉ lưu trường 'url'
        'encoding': 'utf-8', # Đảm bảo mã hóa UTF-8
    }
}

# Thêm vào settings.py
SPLASH_URL = 'http://localhost:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'


# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
