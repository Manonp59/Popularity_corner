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
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        items = BoxOfficeItem()
        
        items["title"] = response.css('#content-layout > section.section.section-wrap.gd-3-cols.gd-gap-20 > div.gd-col-middle > ul > li:nth-child(3) > div > div.meta.meta-affintiy-score > h2 > a').extract()
        items["entrance"] = 
        items["date_release"] =
        pass
