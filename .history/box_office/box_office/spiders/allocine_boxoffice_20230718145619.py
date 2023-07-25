import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BoxOfficeItem
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy_fake_useragent.middleware import RandomUserAgentMiddleware


class BoxOfficeSpider(CrawlSpider):
    name = 'box_office'
    allowed_domains = ['allocine.fr']
    start_urls = ['https://www.allocine.fr/films/alphabetique/']

    rules = (
        Rule(LinkExtractor(restrict_css='nav.pagination a.button-right'), follow=True),
        Rule(LinkExtractor(restrict_css='section[id="content-layout"] div.mdl div.card>figure.thumb>a'), callback='parse_item'),
    )

    def parse_item(self, response):
        items = BoxOfficeItem()

        items["title"] = response.css('.gd-col-middle ul li.mdl:nth-child(2) h2 a::text').extract()
        yield items
