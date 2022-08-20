# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from twisted.enterprise import adbapi


class JianshuPipeline:
    def __init__(self):
        kwags = {'user': 'root', 'password': 'lxz', 'host': '127.0.0.1', 'port': 3306, 'database': 'jianshu',
                 'charset': 'utf8'}
        self.conn = pymysql.connect(**kwags)
        self.cursor = self.conn.cursor()
        self.sql_str = None

    @property
    def sql(self):
        if self.sql_str is None:
            self.sql_str = """insert into article(title,author,pub_time,word_count,read_count,
                like_count,content,comment_count,subject,article_id,origin_url) 
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
            return self.sql_str
        return self.sql_str  # 这个必须要返回，否则到了execute方法时sql返回空类型会报错

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (
            item['title'], item['author'], item['pub_time'], item['content'], item['article_id'], item['origin_url']))
        self.conn.commit()
        return item


class TwistedJianshuPipeline:
    """  Twisted异步实现存进数据库中  """

    def __init__(self):
        kwags = {'user': 'root', 'password': 'lxz', 'host': '127.0.0.1', 'port': 3306, 'database': 'jianshu',
                 'charset': 'utf8', 'cursorclass': pymysql.cursors.DictCursor}
        self.sql_str = None
        self.db_pool = adbapi.ConnectionPool('pymysql', **kwags)

    @property
    def sql(self):
        if self.sql_str is None:
            self.sql_str = """insert into article(title,author,pub_time,word_count,read_count,
                like_count,content,comment_count,subject,article_id,origin_url) 
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
            return self.sql_str
        return self.sql_str  # 这个必须要返回，否则到了execute方法时sql返回空类型会报错

    def process_item(self, item, spider):  # 把提交SQL语句放进runInteraction里实现异步
        defer = self.db_pool.runInteraction(self.insert_item, item)
        defer.addErrback(self.handle_error, item, spider)
        return item

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (item['title'], item['author'], item['pub_time'], item['word_count'], item['read_count'],
                                  item['like_count'], item['content'], item['comment_count'], item['subject'], item['article_id'], item['origin_url']))

    def handle_error(self, error, item, spider):
        print('*' * 10 + 'error' '*' * 10)
        print(error)
        print('*' * 10 + 'error' '*' * 10)
