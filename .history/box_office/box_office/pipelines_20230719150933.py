# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter



class BoxOfficePipeline:
    def process_item(self, item, spider):
                if box_office_raw:
            box_office_cleaned = re.sub(r'\D', '', box_office_raw)
            
            items['entrance'] = box_office_cleaned
        else:
            items['entrance'] = None
        return item
