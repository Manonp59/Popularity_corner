import csv

class CsvPipeline:
    def open_spider(self, spider):
        self.file = open('films.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.file, fieldnames=[
            'title', 'release_date', 'genre', 'duration', 'director',
            'producers', 'cast', 'press_eval', 'viewers_eval', 'age_limit',
            'nationality', 'distributor', 'views', 'box_office_title',
            'box_office_date', 'box_office_first_week', 'box_office_second_week'
        ])
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item

    def close_spider(self, spider):
        self.file.close()
