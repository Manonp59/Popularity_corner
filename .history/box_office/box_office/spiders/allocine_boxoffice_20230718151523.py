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
        Rule(LinkExtractor(restrict_css='    color: #000;
    -webkit-text-size-adjust: 100%;
    --font1: montserratSemiBold,Arial,Sans-Serif;
    --font2: montserratRegular,Arial,Sans-Serif;
    --font3: pompiereRegular,Arial,Sans-Serif;
    --font4: montserratLight,Arial,Sans-Serif;
    --font-title-weight: false;
    -webkit-font-smoothing: antialiased;
    font-family: Arial,Sans-Serif;
    font-size: .8125rem;
    box-sizing: border-box;
    padding-top: 1.25rem;
    min-width: 0;'), callback='parse_item'),
    )

    def parse_item(self, response):
        items = BoxOfficeItem()

        items["title"] = response.css('.gd-col-middle ul li.mdl h2 a::text').extract()
        yield items
