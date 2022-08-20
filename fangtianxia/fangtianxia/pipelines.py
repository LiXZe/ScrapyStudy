# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter


class FangNewhouseJsonLinesPipeline:
    def __init__(self):
        self.newhouse_file = open('newhouse.json', 'wb')
        self.esfhouse_file = open('esfhouse.json', 'wb')
        self.newhouse_exporter = JsonLinesItemExporter(self.newhouse_file, ensure_ascii=False, encoding='utf-8')
        self.esfhouse_exporter = JsonLinesItemExporter(self.esfhouse_file, ensure_ascii=False, encoding='utf-8')

    def process_item(self, item, spider):
        if 'sale' in item.keys():
            self.newhouse_exporter.export_item(item)
        else:
            self.esfhouse_exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.newhouse_file.close()
        self.esfhouse_file.close()
