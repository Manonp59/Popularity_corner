import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BoxOfficeItem
from datetime import datetime, timedelta
from fake_useragent import UserAgent


class BoxOfficeSpider(CrawlSpider):
    name = 'boxspider'
    allowed_domains = ['allocine.fr']

    user_agent = UserAgent().random

    def last_thursday_date(self):
        today = datetime.today()
        last_week = today - timedelta(days=9)
        return last_week.strftime('%Y-%m-%d')

    def start_requests(self):
        last_thursday = self.last_thursday_date()
        page_url = f'https://www.allocine.fr/film/agenda/sem-{last_thursday}/'
        yield scrapy.Request(url=page_url, headers={'User-Agent': self.user_agent})

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[contains(@class, 'gd-col-left')]//ul//li[contains(@class, 'mdl')]//h2//a"), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_xpaths="//nav[@class='pagination cf']//a"), follow=True),
    )

    def parse_item(self, response):
        film_id = response.url.split('=')[-1].split('.')[0]
        box_office_url = f'https://www.allocine.fr/film/fichefilm-{film_id}/box-office/'

        yield scrapy.Request(url=box_office_url, callback=self.parse_box_office, headers={'User-Agent': self.user_agent})
        

    def parse_box_office(self, response):
        items = BoxOfficeItem()
        date = self.last_thursday_date()

        items["title"] = response.xpath("//div[@class='titlebar-title titlebar-title-lg']//span[1]/text()").get()
        items["week"] = f"{date}"
        items["country"] = response.xpath("//h2[@class='titlebar-title titlebar-title-md']/text()").get()
        
        box_office_raw = response.css('.gd-col-left section:nth-of-type(1) tr:nth-of-type(1) td.second-col::text').extract_first()[1:-1].replace(' ',"")
        
        items['entrance'] = box_office_raw
        yield items