import requests
from lxml import etree
import time

headers = {'authority': 'www.zhipin.com',
           'method': 'GET',
           'path': '/job_detail/9bf7f88172e2941d1XR63NW6ElFQ.html',
           'scheme': 'https',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'zh-CN,zh;q=0.9',
           'cache-control': 'max-age=0',
           'cookie': 'Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1647745384,1648210751; __g=-; lastCity=100010000; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1648215625; __c=1648210751; __l=l=%2Fwww.zhipin.com%2Fjob_detail%2F9bf7f88172e2941d1XR63NW6ElFQ.html&r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DFU_t7twbaX_qnfLJsy-hS8cTL-H9KJEFAYUrL7P2AKRvkMXHMKZagyrIUQWwmmSY%26wd%3D%26eqid%3Ddf6c60d6000002ba00000006623db322&g=&s=3&friend_source=0&s=3&friend_source=0; __a=93582919.1647745384.1647745384.1648210751.13.2.11.13; __zp_stoken__=956fdGmBcSTwGZHcQPW9pCHFMRlYCbFthWCcxc3IkcXd4SS1TdRZdExlOTQx4LAghQX9fCQx7H35%2BQi88LS0ON3YVNlZuaDcDOjkZcwxBM2IDGBtdby49ZhREZmZHIUFqA0ZtfQx9NANBfiE%3D',
           'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
           'sec-ch-ua-mobile': '?0',
           'sec-ch-ua-platform': '"Windows"',
           'sec-fetch-dest': 'document',
           'sec-fetch-mode': 'navigate',
           'sec-fetch-site': 'none',
           'sec-fetch-user': '?1',
           'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
           }
url = 'https://www.zhipin.com/job_detail/9bf7f88172e2941d1XR63NW6ElFQ.html'
response = requests.get(url, headers=headers)
time.sleep(3)
data = response.content.decode()
print(data)
# html = etree.HTML(data)
# lis = html.xpath('//div[@class="text"]/text()')
# print(lis)
