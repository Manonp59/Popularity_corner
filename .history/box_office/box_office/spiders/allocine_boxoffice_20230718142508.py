import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_fake_useragent.middleware import RandomUserAgentMiddleware
from ..items import BoxOfficeItem

class BoxOfficeSpider(CrawlSpider):
    name = 'box_office'
    allowed_domains = ['allocine.fr']
    start_urls = ['https://www.allocine.fr/films/alphabetique/']


    rules = (
        Rule(LinkExtractor(restrict_css='section[id="content-layout"] div.mdl div.card>figure.thumb>a'), callback='parse_item'),
        Rule(LinkExtractor(restrict_css='nav.pagination a.button-right'), follow=True),
    )

    def parse_item(self, response):
        items = BoxOfficeItem()

        items["title"] = response.css('h1.titlebar-title::text').get().strip()
        yield items
