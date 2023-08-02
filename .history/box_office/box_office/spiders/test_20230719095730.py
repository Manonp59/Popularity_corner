import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BoxOfficeItem
from datetime import datetime, timedelta


class BoxOfficeSpider(CrawlSpider):
    name = 'box'
    allowed_domains = ['allocine.fr']

    user_agent_list = [
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15',
        'Mozilla/5.0 (iPad; CPU iPadOS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/605.1.15',
    ]

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
        data = self.last_thursday_date()
        
        items["title"] = response.css('div.titlebar-title.titlebar-title-lg::text').get().strip()
        items["week"] = "last_thursday"
        yield items