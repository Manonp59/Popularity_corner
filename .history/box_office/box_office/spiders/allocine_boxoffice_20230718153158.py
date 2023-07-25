import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BoxOfficeItem, EntranceItem
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy_fake_useragent.middleware import RandomUserAgentMiddleware


class BoxOfficeSpider(CrawlSpider):
    name = 'box_office'
    allowed_domains = ['allocine.fr']
    start_urls = ['https://www.allocine.fr/films/alphabetique/']

    rules = (
        # La première règle pointe vers la page de chaque film.
        Rule(LinkExtractor(restrict_css='div.gd-col-middle ul li.mdl h2 a'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        items = BoxOfficeItem()

        # Récupération du titre du film
        items["title"] = response.css('div.titlebar-title.titlebar-title-lg::text').get().strip()

        # Extraction de l'URL de la page Box-office du film
        box_office_url = response.url.replace('fichefilm_gen_cfilm', 'film/fichefilm') + 'box-office/'

        # Transmission des items pour le prochain callback avec l'URL box-office
        request = scrapy.Request(box_office_url, callback=self.parse_score)
        request.meta['item'] = items
        yield request

        
    def parse_score(self, response):
        items = response.meta['item']
        items = EntranceItem()
        
        # Assurez-vous que votre sélecteur pointe vers le bon tbody
        first_row = response.css('tbody tr.responsive-table-row:first-child')
        items["date_release"] = first_row.css('td.responsive-table-column.first-col span::text').get().strip()
        items["entrance"] = first_row.css('td.responsive-table-column.second-col::text').get().strip()
        
        yield items
