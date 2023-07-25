import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BoxOfficeItem
from datetime import datetime, timedelta
from fake_useragent import UserAgent


class BoxOfficeSpider(CrawlSpider):
    name = 'box'
    allowed_domains = ['allocine.fr']

    user_agent = Us

    def last_thursday_date(self):
        today = datetime.today()
        offset = (today.weekday() - 3) % 7
        last_thursday = today - timedelta(days=offset)
        return last_thursday.strftime('%Y-%m-%d')

    def start_requests(self):
        last_thursday = self.last_thursday_date()
        page_url = f'https://www.allocine.fr/film/agenda/sem-{last_thursday}/'
        yield scrapy.Request(url=page_url, headers={'User-Agent': self.user_agent_list[0]})

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[contains(@class, 'gd-col-left')]//ul//li[contains(@class, 'mdl')]//h2//a"), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_xpaths="//nav[@class='pagination cf']//a"), follow=True),
    )

    def parse_item(self, response):
        items = BoxOfficeItem()
        date = self.last_thursday_date()
        
        items["title"] = response.css('div.titlebar-title.titlebar-title-lg::text').get().strip()
        items["week"] = f"{date}"
        yield items