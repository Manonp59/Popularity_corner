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
        Rule(LinkExtractor(restrict_css='div.gd-col-middle'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_css='nav.pagination a.button-right'), follow=True),
    )

    def parse_item(self, response):
        items = BoxOfficeItem()

        items["title"] = response.css('ul > li.mdl > h2 > a::text').extract()
        yield items
