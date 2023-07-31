import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import random

class FilmsSpider(CrawlSpider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'popularity_corner.pipelines.CsvPipeline': 300,
        }
    }

    name = 'films'
    allowed_domains = ['allocine.fr']

    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    ]

    def start_requests(self):
        base_url = 'https://www.allocine.fr/films/?page='
        num_pages = 7691  # Modify the desired number of pages, e.g., 7691
        for page in range(1, num_pages + 1):
            url = base_url + str(page)
            yield scrapy.Request(url=url, headers={'User-Agent': random.choice(self.user_agent_list)})

    rules = (
        Rule(LinkExtractor(restrict_css='h2 a'), callback='parse_item'),
        Rule(LinkExtractor(restrict_css='.pagination-item-next'), follow=True),
    )

    @staticmethod
    def delete_views(views: str):
        final = ""
        for v in views:
            if v in '1234567890':
                final += v
        return int(final)

    @staticmethod
    def clean_views(views):
        if isinstance(views, list):
            return max([FilmsSpider.delete_views(v) for v in views])
        elif isinstance(views, str):
            return FilmsSpider.delete_views(views)
        return None

    def parse_item(self, response):
        item = {}
        original_title = response.css("div.meta-body-item:nth-of-type(5)::text").extract()
        if original_title:
            filtered_title = [title for title in original_title if re.search(r'[a-mo-z]', title, re.IGNORECASE)]
            if filtered_title:
                final_title = filtered_title[0][1:-1]
            else:
                final_title = response.css('div.titlebar-title::text').extract_first()
        else:
            final_title = response.css('div.titlebar-title::text').extract_first()
        item['title'] = final_title
        evaluations = response.css("div.rating-item-content span.stareval-note::text").extract() 
        release_date = response.css('span.date.blue-link::text').get()
        item['release_date'] = release_date.strip() if release_date else None
        genres = response.css('div.meta-body-item.meta-body-info span::text').getall()
        item['genre'] = [genre.strip() for genre in genres[3:]] if genres else None
        duration = response.css('div.meta-body-item.meta-body-info::text').re_first(r'(\d+h \d+min)')
        item['duration'] = duration if duration else None
        director = response.css('.meta-body-item.meta-body-direction span.blue-link::text').get()
        item['director'] = director if director else None
        producers = response.css('.meta-body-item.meta-body-direction span.blue-link::text').getall()[1:]
        item['producers'] = producers if producers else None
        cast = response.css('.meta-body-item.meta-body-actor span::text').getall()[1:]
        item['cast'] = cast if cast else None
        item['press_eval'] = evaluations[0] if evaluations else None
        item['viewers_eval'] = evaluations[1] if len(evaluations) > 1 else None
        age_limit = response.css('.label.kids-label::text').get()
        age_limit_adult = response.css('span.certificate-text::text').get()
        item['age_limit'] = age_limit.strip() + ' (children\'s film)' if age_limit else age_limit_adult
        nationality = response.css('span.nationality::text').get()
        item['nationality'] = nationality.strip() if nationality is not None else None
        item['distributor'] = response.css('span.that.blue-link::text').get().strip() if response.css(
            'span.that.blue-link::text').get() else None
        views = response.css("div.meta-sub.light > span::text").extract()
        item['views'] = self.clean_views(views) if views else None

        # Extract the film ID from the URL
        film_id = response.url.split('=')[-1].split('.')[0]

        # Construct the box office URL: "https://www.allocine.fr/film/fichefilm-180899/box-office/"
        box_office_url = f'https://www.allocine.fr/film/fichefilm-{film_id}/box-office/'

        # Send a request to scrape the box office page
        yield scrapy.Request(url=box_office_url, callback=self.parse_box_office, meta={'item': item})
        

    def parse_box_office(self, response):
        item = response.meta.get('item', {})
        item['box_office_title'] = response.css('.gd-col-left section:nth-of-type(1) h2::text').extract()
        box_office_date = response.css('td.responsive-table-column.first-col span.blue-link::text').extract()
        box_office_first_raw = response.css('.gd-col-left section:nth-of-type(1) tr:nth-of-type(1) td::text').extract()
        box_office_second_raw = response.css('.gd-col-left section:nth-of-type(1) tr:nth-of-type(2) td::text').extract()

        # Clean box_office_date list
        item['box_office_date'] = [date.strip() for date in box_office_date][0:2]

        # Clean box_office_second_raw list
        box_office_second_cleaned = [value.strip() for value in box_office_second_raw if value.strip()]
        item['box_office_second_week'] = box_office_second_cleaned[0] if box_office_second_cleaned else None
            
        # Clean box_office_first_raw list
        box_office_first_cleaned = [value.strip() for value in box_office_first_raw if value.strip()]
        item['box_office_first_week'] = box_office_first_cleaned[0] if box_office_first_cleaned else None

        yield item
