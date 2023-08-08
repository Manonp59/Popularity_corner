import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_fake_useragent.middleware import RandomUserAgentMiddleware
from ..items import BoxOfficeItem

class BoxOfficeSpider(CrawlSpider):
    name = 'box_office'
    allowed_domains = ['allocine.fr']
    start_urls = ['https://www.allocine.fr/films/alphabetique/']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        }
    }

    rules = (
        Rule(LinkExtractor(restrict_css=('//div[contains(@class, "gd-col-middle"')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        items = BoxOfficeItem()
        
        items["title"] = response.css('//div[contains(@c]').extract()
        items["date_release"] = response.xpath('//a[contains(@class, "xXx") and contains(@class, "item") and contains(@class, "first-col") and contains(@class, "blue-link")][1]/text()').extract()
        items["entrance"] = response.xpath('//a[contains(@class, "responsive-table-column") and contains(@class, "second-col") and contains(@class, "col-bg")][1]/text()').extract()
        yield items
