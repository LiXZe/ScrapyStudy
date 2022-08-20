import scrapy
import re
from fangtianxia.items import NewHouseItem, esfItem


class FangSpider(scrapy.Spider):
    name = 'fang'
    allowed_domains = ['fang.com']
    start_urls = ['https://www.fang.com/SoufunFamily.htm']

    def parse(self, response):
        trs = response.xpath('//div[@class="outCont"]//tr')
        province = None
        for tr in trs:
            province_xpath = tr.xpath('.//td[@valign="top"]/strong/text()').get()
            if province_xpath is not None and province_xpath != '\xa0':  # 空格的Unicode编码是'\xa0'
                province = province_xpath
            if province == '其它':  # 只爬取国内城市的房源信息
                continue
            # print('\n' + province + ':')
            tds = tr.xpath('.//td/a')
            for td in tds:
                city = td.xpath('.//text()').get()
                href = td.xpath('./@href').get()
                temp_url = href.split('fang')[0]
                newhouse_url = temp_url + 'newhouse.fang.com/house/s/'
                esf_url = temp_url + 'esf.fang.com'
                # print(city + ':' + newhouse_url + ' ' + esf_url, end=',')
                yield scrapy.Request(url=newhouse_url, callback=self.parse_newhouse, meta={'info': (province, city)})
                yield scrapy.Request(url=esf_url, callback=self.parse_esf, meta={'info': (province, city)})
                # break
            break

    def parse_newhouse(self, response):  # 一堆\t\n
        province, city = response.meta.get('info')
        lis = response.xpath('//div[@class="nl_con clearfix"]//li')
        for li in lis:
            name = li.xpath('.//div[@class="nlcd_name"]/a/text()').get()
            if name is None:
                continue
            name = name.strip()
            rooms = '/'.join(li.xpath('.//div[@class="house_type clearfix"]/a/text()').getall())
            area = re.sub(r'\n|\t|\s|/|—', '', ''.join(li.xpath('.//div[@class="house_type clearfix"]/text()').getall()))
            district = re.sub(r'\n|\t|\[|\]', '', ''.join(li.xpath('.//div[@class="address"]//a/span/text()').getall()))
            address = li.xpath('.//div[@class="address"]//a/@title').get()
            price_xpath = li.xpath('.//div[@class="nhouse_price"]/span/text()').get()
            unit = li.xpath('.//div[@class="nhouse_price"]/em/text()').get()
            if price_xpath is not None and unit is not None:  # 这俩个值均有可能为空
                price = price_xpath + unit
            else:
                price = ''
            sale = re.sub(r'\n|\t|\[|\]', '', li.xpath('.//div[@class="fangyuan"]/span/text()').get())
            detail_url = li.xpath('.//div[@class="nlcd_name"]/a/@href').get()
            # print(name + ':' + rooms + ':' + area + ':' + district + ':' + address + ':' + price + ':' + sale + ':'
            #  + detail_url)
            yield NewHouseItem(province=province, city=city, name=name, rooms=rooms, area=area, district=district,
                               address=address, price=price, sale=sale, detail_url=detail_url)
        next_url = response.xpath('//div[@class="page"]//a[text()="下一页"]/@href').get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_newhouse,
                                 meta={'info': (province, city)})

    def parse_esf(self, response):
        province, city = response.meta.get('info')
        item = esfItem(province=province, city=city)
        dls = response.xpath('//div[@class="shop_list shop_list_4"]//dl[@class="clearfix"]')
        for dl in dls:  # 需要提取的数据没有固定的排序
            dds1 = dl.xpath('.//dd[1]')
            infos = list(map(lambda x: re.sub('\t|\n', '', x), dds1.xpath('.//p[@class="tel_shop"]/text()').getall()))
            item['room_type'] = dds1.xpath('.//p[@class="tel_shop"]/a/text()').get()  # 有独栋和联排的情况
            for info in infos:
                if info is None:
                    continue
                if '厅' in info:
                    item['rooms'] = info
                elif '卧' in info:
                    item['rooms'] = info
                elif '㎡' in info:
                    item['area'] = info
                elif '层' in info:
                    item['floor'] = re.sub(r'（|）', '', info)
                elif '向' in info:
                    item['toward'] = info
                elif '建' in info:
                    item['year'] = info
            name = dds1.xpath('.//p[@class="add_shop"]//a/text()').get()
            if name is not None:
                item['name'] = re.sub(r'\t|\n', '', name)
            else:
                item['name'] = ''
            item['address'] = dds1.xpath('.//p[@class="add_shop"]//span/text()').get()
            dds2 = dl.xpath('.//dd[2]')
            price_xpath = dds2.xpath('.//span[@class="red"]').get()
            if price_xpath is not None:
                item['price'] = re.sub(r'<span class="red">|\t|\n|<b>|</b>|</span>', '', price_xpath)
            else:
                item['price'] = ''
            item['unit_price'] = dds2.xpath('.//span[2]/text()').get()
            item['detail_url'] = response.urljoin(dds1.xpath('.//h4[@class="clearfix"]//a/@href').get())
            # print(item)
            yield item
        # 解析下一页
        next_url = response.xpath('//div[@class="page_box"]//p/a[text()="下一页"]/@href').get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_esf,
                                 meta={'info': (province, city)})
