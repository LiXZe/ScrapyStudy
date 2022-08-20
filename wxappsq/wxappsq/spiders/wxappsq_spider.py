import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wxappsq.items import WxappsqItem
"""爬取小程序社区中所有文章的 标题、作者、时间、文章内容"""


class WxappsqSpiderSpider(CrawlSpider):
    name = 'wxappsq_spider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['https://www.wxapp-union.com/portal.php?mod=list&catid=1&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+mod=list&catid=1&page=\d'), follow=True),
        Rule(LinkExtractor(allow=r'.+article-.+\.html'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        title = response.xpath('//h1[@class="ph"]/text()').get()
        author = response.xpath('//p[@class="authors"]/a/text()').get()
        article_time = response.xpath('//p[@class="authors"]/span/text()').get()
        article_content = response.xpath('//td[@id="article_content"]//p/text()').getall()
        item = WxappsqItem(title=title, author=author, article_time=article_time, article_content=article_content)
        yield item
