import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BoxOfficeItem
from fake_useragent import UserAgent


class BoxOfficeSpider(CrawlSpider):
    name = 'box_office'
    allowed_domains = ['allocine.fr']
    start_urls = ['https://www.allocine.fr/films/alphabetique/']

    user_agent = UserAgent()

    rules = (
        Rule(LinkExtractor(restrict_css='section[id="content-layout"] div.mdl div.card>figure.thumb>a'), callback='parse_item'),
        Rule(LinkExtractor(restrict_css='nav.pagination a.button-right'), follow=True),
    )
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.allocine.fr/films/alphabetique/', callback=self.parse_item, )

    def parse_item(self, response):
        items = BoxOfficeItem()

        items["title"] = response.css('h1.titlebar-title::text').get().strip()
        yield items
