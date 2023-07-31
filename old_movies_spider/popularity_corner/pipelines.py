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
        self.file = open('data_movies_final.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['title', 'release_date', 'genre', 'duration', 'director', 'producers', 'cast',
                              'age_limit', 'nationality', 'distributor', 'box_office_title', 'box_office_date',
                              'box_office_first_week', 'box_office_second_week', 'press_eval', 'viewers_eval', 'views'])

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        title = str(item.get('title', ''))
        release_date = str(item.get('release_date', ''))
        genre = ', '.join(item.get('genre', []))
        duration = str(item.get('duration', '')).strip()
        director = str(item.get('director', '')).strip()
        producers = ', '.join(item.get('producers', []))
        cast = ', '.join(item.get('cast', []))
        age_limit = str(item.get('age_limit', ''))
        nationality = str(item.get('nationality', '')).strip()
        distributor = item.get('distributor')
        distributor = str(distributor.strip()) if distributor is not None else ''
        box_office_title = ', '.join(item.get('box_office_title', []))
        box_office_date = str(item.get('box_office_date', '')).strip()
        box_office_first_week = str(item.get('box_office_first_week', '')).strip()
        box_office_second_week = str(item.get('box_office_second_week', '')).strip()
        press_eval = str(item.get('press_eval', ''))
        viewers_eval = str(item.get('viewers_eval', ''))
        views = str(item.get('views', ''))

        self.writer.writerow([title, release_date, genre, duration, director, producers, cast, age_limit,
                              nationality, distributor, box_office_title, box_office_date, box_office_first_week,
                              box_office_second_week, press_eval, viewers_eval, views])
        return item
