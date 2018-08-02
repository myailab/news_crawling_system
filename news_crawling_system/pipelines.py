# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import pymysql

class NewsCrawlingSystemPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            user="root",
            password="123456",
            port=3306,
            host="127.0.0.1",
            db="news_crawling",
            charset="utf8"
        )

    def process_item(self, item, spider):
        print(item)
        self.insert_news(item)
        print(item)
        return item

    def insert_news(self, items):
        """
        将新闻数据插入到news_info表中

        :param items:
        :return:
        """
        cur = self.connect.cursor()  # 获取游标
        # 创建或更新时间
        create_or_update_time = time.strftime("%Y-%m-%d")
        website_id = 1

        # 查询对应的staff_md5是否存在,如果存在,则不插入,如果不存在,则插入
        query_sql = "select id from news_info where news_md5='%s'"
        effect_row = cur.execute(query_sql % items['news_md5'])
        if effect_row == 0:
            insert_sql = "INSERT INTO news_info (news_md5, title, news_date, source, body, create_time, website_id) " \
                         "VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"
            try:
                cur.execute(insert_sql % (items['news_md5'], items['title'], items['date_time'], items['news_source'],
                                          items['news_body'], create_or_update_time, website_id))
                # 提交
                self.connect.commit()
            except:
                # 回滚
                self.connect.rollback()
                pass