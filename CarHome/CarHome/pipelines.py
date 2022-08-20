# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
from urllib import request
import re


class BcPipeline:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'GaoQin_image_HQhs7')  # D:\Scrapy-Study\BC

    # 下载高清图
    def process_item(self, item, spider):
        title = item['title']
        urls = item['urls']
        title_path = os.path.join(self.path, title)
        if not os.path.exists(title_path):
            os.mkdir(title_path)
        for url in urls:
            pattern = re.compile(r'..............................\.jpg')
            result = pattern.findall(url)
            image_name = result[0]
            request.urlretrieve(url, os.path.join(title_path, image_name))
        return item

    # 旧版
    # def process_item(self, item, spider):
    #     title = item['title']
    #     urls = item['urls']
    #     title_path = os.path.join(self.path, title)
    #     if not os.path.exists(title_path):
    #         os.mkdir(title_path)
    #     for url in urls:
    #         image_name = url.split('__')[1]
    #         request.urlretrieve(url, os.path.join(title_path, image_name))
    #     return item
