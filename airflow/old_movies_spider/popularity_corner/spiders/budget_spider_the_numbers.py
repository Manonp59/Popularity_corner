import scrapy
import re 

class BudgetSpider(scrapy.Spider):
    name = 'budget'
    
    allowed_domains = ['the-numbers.com']
    
    start_urls = ['https://www.the-numbers.com/movie/budgets/all']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    def start_requests(self):
        base_url = 'https://www.the-numbers.com/movie/budgets/all'
        links_to_scrape = [base_url]
        # Boucle pour générer les liens de 101 à 6401 avec un pas de 100
        for page_num in range(101, 6501, 100):
            url = f"{base_url}/{page_num}"
            links_to_scrape.append(url)
        
        for url in links_to_scrape:
            yield scrapy.Request(url, callback=self.parse,headers={'User-Agent': self.user_agent})

    def parse(self, response):
        for row in response.css('table tr')[1:]:
            release_date = row.css('td:nth-child(2) a::text').get()
            movie = row.css('td:nth-child(3) b a::text').get()
            production_budget = row.css('td:nth-child(4)::text').get()
            
            production_budget = re.sub(r'[^\d]', '', production_budget)

            yield {
                'Release Date': release_date,
                'Movie': movie,
                'Production Budget': production_budget,
            }
        


    