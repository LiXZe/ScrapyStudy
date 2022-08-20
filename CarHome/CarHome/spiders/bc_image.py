import scrapy
from BC.items import BcItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re


class BcImageSpider(CrawlSpider):
    name = 'bc_image'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/4150.html#pvareaid=3454438']

    rules = (  # 要下载到“下一页”的图片allow里的地址不能写全，因为网页里的地址也没写全
        Rule(LinkExtractor(allow=r'/pic/series/4150.+'), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        title = response.xpath('//div[@class="uibox"]/div[@class="uibox-title"]/text()').get()
        if not self.chi_title(title):
            return
        urls = response.xpath('//div[@class="uibox"]//ul/li//img/@src').getall()
        urls = list(map(lambda url: response.urljoin(url.replace('480x360_0_q95_c42_autohomecar__', '')), urls))
        item = BcItem(title=title, urls=urls)
        yield item

    def chi_title(self, title):  # 判断title是否为中文
        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        result = pattern.findall(title)
        if len(result) is 0:
            return False
        else:
            return True

    """  CrawlSpider会继承scrapy.spiders的parse方法  """
    # def parse(self, response):
    #     divs = response.xpath('//div[@class="uibox"]')[1:]
    #     for div in divs:
    #         title = div.xpath('.//div[@class="uibox-title"]/a/text()').get()
    #         urls = div.xpath('.//li/a/img/@src').getall()
    #         urls = list(map(lambda url: response.urljoin(url), urls))
    #         item = BcItem(title=title, urls=urls)
    #         yield item
