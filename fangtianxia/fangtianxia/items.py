# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()  # 小区名
    rooms = scrapy.Field()  # 几居
    area = scrapy.Field()  # 面积
    district = scrapy.Field()  # 行政区
    address = scrapy.Field()  # 地址
    price = scrapy.Field()
    sale = scrapy.Field()  # 是否在售
    detail_url = scrapy.Field()  # 详情URL地址


class esfItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    room_type = scrapy.Field()  # 房子类型，独栋或者联排，还是在高层
    rooms = scrapy.Field()  # 几居
    area = scrapy.Field()
    floor = scrapy.Field()
    toward = scrapy.Field()
    year = scrapy.Field()
    name = scrapy.Field()  # 小区名
    address = scrapy.Field()  # 地址
    price = scrapy.Field()
    unit_price = scrapy.Field()
    detail_url = scrapy.Field()  # 详情URL地址
