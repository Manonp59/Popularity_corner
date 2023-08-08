import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BoxOfficeItem #EntranceItem
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy_fake_useragent.middleware import RandomUserAgentMiddleware


class BoxOfficeSpider(CrawlSpider):
    name = 'box_office'
    allowed_domains = ['allocine.fr']
    start_urls = ['https://www.allocine.fr/films/alphabetique/']
    
    num_pages = 1  # Modifier le nombre de pages souhaité 7691
    for page in range(1, num_pages + 1):
        url = page_url + str(page)

    rules = (
        Rule(LinkExtractor(restrict_css='div.gd-col-middle'), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_css='nav.pagination a.button-right'), follow=True),
        # Rule(LinkExtractor(allow="box-office/"), callback='parse_score')
    )

    def parse_item(self, response):
        items = BoxOfficeItem()

        items["title"] = response.css('ul li.mdl h2 a::text').extract()
        yield items
        
        
    # def parse_score(self, response):
    #     items = EntranceItem()
        
    #     # Assurez-vous que votre sélecteur pointe vers le bon tbody
    #     first_row = response.css('tbody tr.responsive-table-row:first-child')
    #     items["date_release"] = first_row.css('td.responsive-table-column.first-col span::text').get().strip()
    #     items["entrance"] = first_row.css('td.responsive-table-column.second-col::text').get().strip()
        
    #     yield items
