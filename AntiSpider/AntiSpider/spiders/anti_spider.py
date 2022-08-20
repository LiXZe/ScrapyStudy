import scrapy
import json
"""反爬虫：在”下载器中间件“中设置随机请求头和IP代理池"""


class AntiSpiderSpider(scrapy.Spider):
    name = 'anti-spider'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/user-agent']
    # start_urls = ['http://httpbin.org/ip']

    def parse(self, response):
        print('*' * 40)
        user_agent = json.loads(response.text)['user-agent']
        print(user_agent)
        # ip = json.loads(response.text)['origin']
        # print(ip)
        print('*' * 40)
        # 重复请求时 dont_filter 防止调度器过滤掉重复的URL
        yield scrapy.Request(self.start_urls[0], dont_filter=True)
