import scrapy


class myitem(scrapy.Item):
    a = scrapy.Field()
    b = scrapy.Field()

item = myitem(a='123', b='456')
# item['a'] = '123'
# item['b'] = '456'
print(type(item))
print('a' in item.keys())
# 计算日期

