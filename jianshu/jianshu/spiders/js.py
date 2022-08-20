import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu.items import JianshuItem
import json
"""爬取 “简书” 所有文章的标题、作者、发布时间、字数、阅读数、点赞数、文章内容(包括HTML标签)、分类、文章ID、文章链接后放入MySQL数据库"""


class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/p/[0-9a-z]{12}.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print('*' * 40)
        title = response.xpath('//h1[@class="_1RuRku"]/text()').get()
        json_author = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        data_author = json.loads(json_author)
        author = data_author['props']['initialState']['note']['data']['user']['nickname']
        pub_time = response.xpath('//div[@class="s-dsoj"]//time/text()').get()  # ajax获得
        word_count = response.xpath('//div[@class="s-dsoj"]/span/text()').getall()[0].split('字数 ')[1].replace(',', '')  # ajax获得
        read_count = response.xpath('///div[@class="s-dsoj"]/span/text()').getall()[1].split('阅读 ')[1].replace(',', '')  # ajax获得
        like_count = response.xpath('//span[@class="_1LOh_5"]/text()').get().split('人点赞')[0].replace(',', '')  # ajax获得
        content = response.xpath('//article[@class="_2rhmJa"]').getall()  # 把HTML标签也返回
        comment_count = response.xpath('//div[@class="_3nj4GN"]/span/text()').getall()[1].replace(',', '')  # ajax获得
        subject = ','.join(response.xpath('//span[@class="_2-Djqu"]/text()').getall())  # MySQl无法添加list列表中一段一段分隔开的的数据，需要用join把列表连接成字符串
        article_id = response.url.split('/')[-1]
        origin_url = response.url
        yield JianshuItem(title=title, author=author, pub_time=pub_time, word_count=word_count, read_count=read_count,
                          like_count=like_count, content=content, comment_count=comment_count,
                          subject=subject, article_id=article_id, origin_url=origin_url)
