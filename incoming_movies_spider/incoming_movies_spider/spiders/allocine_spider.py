import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_fake_useragent.middleware import RandomUserAgentMiddleware
from ..items import IncomingMovieItem
from .utils import clean_date, clean_views
from datetime import date, datetime

class AllocineSpider(CrawlSpider):
    name = 'incomingmovies'
    allowed_domains = ['allocine.fr']
    start_urls = ['https://www.allocine.fr/film/agenda/']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        },
        "FEEDS" : {
            "next_week.csv": {
                "format": "csv", 
                "overwrite": True
            }
        }
    }
    

    rules = (
        Rule(LinkExtractor(restrict_css=".meta-title-link"), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        release_date = clean_date(response.css('.date::text').extract())
        if release_date >= date.today():
            original_title = response.css("div.meta-body-item:nth-of-type(5)::text").extract()
            genres = response.css('div.meta-body-item.meta-body-info span::text').getall()
            evaluations = response.css("div.rating-item-content span.stareval-note::text").extract()
            if not evaluations:
                evaluations = [None, None]


            if original_title:
                final_title = original_title[1][1:-1]
            else:
                final_title = response.css('.titlebar-title-lg::text').extract()
            
            
            # print("#"*50 ,"\n",
            #       response.css(".meta-body-item.meta-body-info::text").extract(),
            #       "\n","#"*50)


            item = IncomingMovieItem(
                release_date = clean_date(response.css('.date::text').extract()),
                title = final_title,
                director = response.css(".meta-body-direction span.blue-link::text").extract(),
                main_actors = response.css(".meta-body-actor span::text").extract()[1:],
                press_eval = evaluations[0],
                viewers_eval = evaluations[1],
                duration = response.css(".meta-body-item.meta-body-info::text").extract()[3].replace('\n', ''),
                views = clean_views(response.css("div.meta-sub.light > span::text").extract()),
                genres = [genre.strip() for genre in genres[3:]],
                nationality = response.css('span.nationality::text').get().strip(),
                distributor = response.css('span.that.blue-link::text').get().strip() if response.css('span.that.blue-link::text').get() else None
            )

            yield item