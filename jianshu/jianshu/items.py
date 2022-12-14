# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    pub_time = scrapy.Field()
    word_count = scrapy.Field()
    read_count = scrapy.Field()
    like_count = scrapy.Field()
    content = scrapy.Field()
    comment_count = scrapy.Field()
    subject = scrapy.Field()
    article_id = scrapy.Field()
    origin_url = scrapy.Field()
