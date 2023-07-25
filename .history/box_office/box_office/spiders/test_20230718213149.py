import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BoxOfficeItem


class BoxOfficeSpider(CrawlSpider):
    name = 'box'
    allowed_domains = ['allocine.fr']

    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'

    def start_requests(self):
        page_url = 'https://www.allocine.fr/films/alphabetique/?page='
        num_pages = 1  # Modifier le nombre de pages souhaité
        for page in range(1, num_pages + 1):
            url = page_url + str(page)
            yield scrapy.Request(url=url, headers={'User-Agent': self.user_agent})

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[contains(@class, 'gd-col-middle')]//ul//li[contains(@class, 'mdl')]//h2//a"), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_xpaths=f"//a[@href='/films/alphabetique/?page=']"), follow=True),
    )

    def parse_item(self, response):
        items = BoxOfficeItem()

        items["title"] = response.css('div.titlebar-title.titlebar-title-lg::text').get().strip()

        yield items
