import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import random

class MoviesBudget(CrawlSpider):
    
    name = 'budget_imdb2'
    allowed_domains = ['imdb.com']

    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    ]
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?title_type=feature&release_date=2000-01-01,')

    rule_pagination = Rule(LinkExtractor(restrict_css='.lister-page-next.next-page'), follow=True)

    films_link = LinkExtractor(restrict_css='.lister-item-content h3 a')

    
    rule_film_details = Rule(films_link, callback='parse_item', follow=False)


    rules = [
        rule_pagination,
        rule_film_details
    ]
    
    def process_pagination_links(self, response):
        next_page_urls = response.css('.lister-page-next.next-page::attr(href)').getall()
        for next_page_url in next_page_urls:
            yield scrapy.Request(next_page_url, callback=self.parse)

    
    def parse_item(self, response):
        
        title = response.css('.sc-afe43def-1::text').get()
        score = response.css('.sc-bde20123-1::text').get()
        genre = response.css('.ipc-chip__text::text').get()
        annee = response.css('.sc-afe43def-4 li:nth-of-type(1) a::text').get()
        duree = response.css("ul.ipc-inline-list li.ipc-inline-list__item:nth-child(3)::text").get()
        acteurs = response.css('a.sc-bfec09a1-1::text').extract()
        public = response.css('.sc-afe43def-4 li:nth-of-type(2) a::text').get()
        pays = response.css('[data-testid="title-details-origin"] a::text').get()
        budget = response.css('li.ipc-metadata-list__item[data-testid="title-boxoffice-budget"] span.ipc-metadata-list-item__list-content-item::text').get()
        
        
           
        if duree:
            match = re.match(r'^(\d+)h\s(\d+)m$', duree.strip())
            if match:
                heures, minutes = match.groups()
                heures = int(heures)
                minutes = int(minutes)
                if heures >= 0 and minutes >= 0:
                    duree_minutes = heures*60 + minutes
                    duree = f"{duree_minutes}m"
                elif heures == 1:
                    duree_minutes = heures*60
                    duree = f"{duree_minutes}m"
            else:
                try:
                    duree_minutes = int(duree.strip())
                    if duree_minutes >= 0:
                        if duree_minutes == 60:
                            duree_minutes = 60
                            duree = f"{duree_minutes}m"
                        else:
                            duree = f"{duree_minutes}m"
                except ValueError:
                    pass
            
        
        
        
        yield {
            'Title': title,
            'Score': score,
            'Genre': genre,
            'Année': annee,
            'Durée': duree,
            'Acteurs': acteurs,
            'Public': public,
            'Pays': pays,
            'Budget':budget
        }