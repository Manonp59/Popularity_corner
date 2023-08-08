import scrapy
import random

class StarsSpider(scrapy.Spider):
    name = 'stars'
    allowed_domains = ['allocine.fr']

    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    ]

    def start_requests(self):
        base_url = 'https://www.allocine.fr/personne/top/les-plus-vues/ever/?page='
        num_pages = 20
        for page in range(1, num_pages + 1):
            url = base_url + str(page)
            headers = {'User-Agent': random.choice(self.user_agent_list)}
            yield scrapy.Request(url=url, headers=headers)

    def parse(self, response):
        for star_card in response.css("li.hred div.meta-title a.meta-title-link"):
            star_name = star_card.css("::text").get()
            yield {"name": star_name.strip()}

        
