# Data_scraper/Data_scraper/settings.py
BOT_NAME = "Data_Scraper"

SPIDER_MODULES = ["Data_Scraper.spiders"]
NEWSPIDER_MODULE = "Data_Scraper.spiders"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 5
CONCURRENT_REQUESTS = 32

# FEEDS để trống, sẽ cấu hình trong spider
FEEDS = {}

DOWNLOADER_MIDDLEWARES = {
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"