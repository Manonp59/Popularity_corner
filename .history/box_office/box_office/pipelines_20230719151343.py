import re
from itemadapter import ItemAdapter



class BoxOfficePipeline:
    def process_item(self, item, spider):
        box_office_raw = item['entrance']
        
        if box_office_raw:
            box_office_cleaned = re.sub(r'\D', '', box_office_raw)
            item['entrance'] = box_office_cleaned
        else:
            item['entrance'] = None
        return item

