# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PopularityCornerPipeline:
    def process_item(self, item, spider):
        return item

import csv

class CsvPipeline:
    def open_spider(self, spider):
        self.file = open('data_movies.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['title', 'release_date', 'genre', 'duration', 'director', 'producers', 'cast',
                              'age_limit', 'nationality', 'distributor', 'box_office_title',
                              'box_office_first_week', 'press_eval', 'viewers_eval', 'views'])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        title = item.get('title', '')
        release_date = item.get('release_date', '')
        genre = ', '.join(item.get('genre', []))
        duration = item.get('duration', '').strip()
        director = item.get('director', '').strip()
        producers = ', '.join(item.get('producers', []))
        cast = ', '.join(item.get('cast', []))
        age_limit = item.get('age_limit', '')
        nationality = item.get('nationality', '').strip()
        distributor = item.get('distributor')
        if distributor is not None:
            distributor = distributor.strip()
        else:
            distributor = ''
        box_office_title = ', '.join(item.get('box_office_title', []))
        box_office_first_week = item.get('box_office_first_week', '').strip()
        press_eval = item.get('press_eval', None)
        viewers_eval = item.get('viewers_eval', None)
        views = item.get('views', '')

        self.writer.writerow([title, release_date, genre, duration, director, producers, cast, age_limit,
                              nationality, distributor, box_office_title, box_office_first_week, press_eval,
                              viewers_eval, views])
        return item