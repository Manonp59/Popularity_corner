import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_fake_useragent.middleware import RandomUserAgentMiddleware

class BoxOfficeSpider(CrawlSpider):
    name = 'box_office'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.co']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        }
    }

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # Parse your items here
        pass
