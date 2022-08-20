# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HospitalnoticeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 公告标题
    body = scrapy.Field()  # 公告内容
    info = scrapy.Field()  # 公告的标头信息
