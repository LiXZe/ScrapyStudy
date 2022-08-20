import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from hospitalNotice.items import HospitalnoticeItem


class NoticeSpider(CrawlSpider):
    name = 'notice'
    allowed_domains = ['sinogene.com.cn']
    start_urls = ['http://www.sinogene.com.cn/news/163.html']

    rules = (  # 要下载到“下一页”的图片allow里的地址不能写全，因为网页里的地址也没写全
        Rule(LinkExtractor(allow=r'/news/163.html?page=\d'), follow=True),
        Rule(LinkExtractor(allow=r'/news_info/\d*.html'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        title = response.xpath('//div[@class="release"]/h1/text()').get()
        items = response.xpath('//div[@class="news_word"]//p//text()').getall()
        infos = response.xpath('//div[@class="release"]/span/text()').get()
        next_url = response.xpath('//a[text()="下一页"]/@href').getall()
        # print(next_url)
        # print(title)
        body = ''
        for item in items:
            it = item.split()
            if isinstance(it, list):
                item = ''
                for i in it:
                    item += i.split()[0]
                body += item
            else:
                body += it
        info = ''
        for i in infos:
            info += i.split()
        # print(body)
        item = HospitalnoticeItem(title=title, body=body, info=info)
        yield item
        if next_url:
            print(+ next_url)
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_item)

