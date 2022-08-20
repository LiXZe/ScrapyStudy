# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter
"""
保存json数据时可以用JsonItemExporter和JsonLinesItemExporter这俩个类，简化操作
JsonItemExporter：每次把树添加到内存中，最后统一写入到磁盘中。好处是存储的是一个满足json规则的数据，坏处是如果数据大，比较耗内存。
JsonLinesItemExporter：每次调用‘export_item’时就把这个item存储到磁盘中。好处是每次处理数据就直接存到了硬盘中，不会耗内存，数据也比较安全。坏处是每一个字典是一行，整个文件不是一个满足json格式的数据。
"""


class WxappsqPipeline:
    def __init__(self):
        self.file = open('wxappsq.json', 'wb')
        self.exporter = JsonLinesItemExporter(file=self.file, ensure_ascii=False, encoding='utf-8')

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.file.close()
