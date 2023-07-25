import scrapy
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BoxOfficeItem
from datetime import datetime, timedelta
from fake_useragent import UserAgent


class BoxOfficeSpider(CrawlSpider):
    name = 'box'
    allowed_domains = ['allocine.fr']

    user_agent = UserAgent().random

    def last_thursday_date(self):
        today = datetime.today()
        offset = (today.weekday() - 3) % 14
        last_thursday = today - timedelta(days=offset)
        return last_thursday.strftime('%Y-%m-%d')

    def start_requests(self):
        last_thursday = self.last_thursday_date()
        page_url = f'https://www.allocine.fr/film/agenda/sem-{last_thursday}/'
        yield scrapy.Request(url=page_url, headers={'User-Agent': self.user_agent})

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[contains(@class, 'gd-col-left')]//ul//li[contains(@class, 'mdl')]//h2//a"), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_xpaths="//nav[@class='pagination cf']//a"), follow=True),
    )

    def parse_item(self, response):
        film_url = response.url
        box_office_url = film_url + 'box-office/'
        yield scrapy.Request(url=box_office_url, callback=self.parse_box_office, headers={'User-Agent': self.user_agent})
        
                # Extraire le numéro du film à partir de l'URL
        film_id = response.url.split('=')[-1].split('.')[0]

        # Construire l'URL du type "https://www.allocine.fr/film/fichefilm-180899/box-office/"
        box_office_url = f'https://www.allocine.fr/film/fichefilm-{film_id}/box-office/'

        # Envoyer une requête pour le scraping de la page de box-office
        yield scrapy.Request(url=box_office_url, callback=self.parse_box_office, meta={'item': item})

    def parse_box_office(self, response):
        item = response.meta.get('item', {})
        item['box_office_title'] = response.css('.gd-col-left section:nth-of-type(1) h2::text').extract()
        yield item

    def parse_box_office(self, response):
        items = BoxOfficeItem()
        date = self.last_thursday_date()

        items["title"] = response.css('div.titlebar-title.titlebar-title-lg::text').get().strip()
        items["week"] = f"{date}"
        box_office_raw = response.css('.gd-col-left section:nth-of-type(1) tr:nth-of-type(1) td.second-col::text').extract_first()
        
        # Extraire le nombre à partir de la chaîne de caractères
        if box_office_raw:
            box_office_cleaned = re.sub(r'\D', '', box_office_raw)
            items['entrance'] = box_office_cleaned
        else:
            items['entrance'] = None

        yield items
