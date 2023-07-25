import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BoxOfficeItem, EntranceItem
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy_fake_useragent.middleware import RandomUserAgentMiddleware


class BoxOfficeSpider(CrawlSpider):
    name = 'box_office'
    allowed_domains = ['allocine.fr']
    start_urls = ['https://www.allocine.fr/films/alphabetique/']

    rules = (
        Rule(LinkExtractor(restrict_css='div.gd-col-middle'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow="box-office/"), callback='parse_score',)
    )

    def parse_item(self, response):
        items = BoxOfficeItem()

        items["title"] = response.css('.gd-col-middle ul li.mdl h2 a::text').extract()
        yield items
        
    def parse_score(self, response):
        items = EntranceItem()
        
        items["date_release"]
        yield items
