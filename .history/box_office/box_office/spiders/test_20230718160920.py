import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BoxOfficeItem


class BoxOfficeSpider(CrawlSpider):
    name = 'box'
    allowed_domains = ['allocine.fr']
    start_urls = ['https://www.allocine.fr/films/alphabetique/']
    
    def start_requests(self):
        page_url = 'https://www.allocine.fr/films/alphabetique/?page='
        num_pages = 1  # Modifier le nombre de pages souhaité 7691
        for page in range(1, num_pages + 1):
            url = page_url + str(page)
            yield scrapy.Request(url=url)

    rules = (
        Rule(LinkExtractor(restrict_css='div.gd-col-middle > ul > li.mdl >h2 a'), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_css='nav.pagination > a.button-right'), follow=False),
    )

    def parse_item(self, response):
        items = BoxOfficeItem()

        items["title"] = response.css('div.titlebar-title.titlebar-title-lg::text').get().strip()

        yield items
