# -*- coding: utf-8 -*-
import scrapy
import hashlib
import configparser
# import urlparse
from news_crawling_system.items import NewsCrawlingSystemItem


class IfengSpider(scrapy.Spider):
    name = 'ifeng'
    allowed_domains = ['ifeng.com']
    start_urls = ['http://www.ifeng.com/']

    def start_requests(self):
        path = "config/ifeng.cfg"
        cf = configparser.ConfigParser()
        cf.read(path)  # 读配置文件（ini、conf）返回结果是列表
        site_list = list(cf.items('ifeng'))

        for category, site in site_list:
            yield scrapy.Request(site, meta={"category": category, "url": site})

    def parse(self, response):
        keys_list = response.meta
        category = keys_list['category']
        # 根据不同的类型调用相应的处理方法
        if category == 'finance':
            url_arr = self.parse_finance_url(response)
            for url in url_arr:
                yield scrapy.Request(url.strip(), callback=self.parse_finance)
        elif category == 'index':
            pass

    def parse_finance_url(self, response):
        # 得到 url的数组
        url_arr = response.xpath('//div[@class="box_02"]/ul[1]//a/@href').extract()
        return url_arr

    def parse_finance(self, response):
        item = NewsCrawlingSystemItem()
        try:
            title = response.xpath("//div[@id='artical']/h1/text()").extract()[0].strip()
            date_time = response.xpath("//div[@id='artical_sth']/p/span[1]/text()").extract()[0].strip()
            news_source = response.xpath("//div[@id='artical_sth']/p/span[3]/span/text()").extract()[0].strip()
            news_body_arr = response.xpath("//div[@id='main_content']//p/text()").extract()
            if len(news_body_arr) >= 2:
                news_body = '<br>'.join(news_body_arr)
            else:
                news_body = news_body_arr[0]
            # 计算信息的md5值,顺序如下:title, date_time
            news_str = title + date_time
            # 创建md5对象
            hl = hashlib.md5()
            hl.update(news_str.encode(encoding='utf-8'))
            news_md5 = hl.hexdigest()
            item['title'] = title
            item['date_time'] = date_time
            item['news_source'] = news_source
            item['news_body'] = news_body
            item['news_md5'] = news_md5
            item['category'] = 'finance'
            return item
        except Exception as e:
            print("Exception:", e)

    def parse_title_2(self, response):
        item = NewsCrawlingSystemItem()
        node = response.xpath("//div[@id='artical']")

        title = node.xpath("./h1/text()").extract()[0].strip()
        date_time_origin = node.xpath("./div/p/span[1]/text()").extract()[0]
        date_time_origin = date_time_origin.replace('年','-')
        date_time_origin = date_time_origin.replace('月','-')
        date_time = date_time_origin.replace('日','')
        news_source = node.xpath("./div/p/span[3]/span//text()").extract()[0]

        # artical_body = node.xpath("//div[@id='main_content']/p[not(@class)]/text()").extract()
        news_body_arr = node.xpath("//div[@id='main_content']/p[not(@class)]").extract()

        if len(news_body_arr) >= 2:
            news_body = '<br>'.join(news_body_arr)
        else:
            news_body = news_body_arr[0]

        # 计算信息的md5值,顺序如下:title, date_time
        news_str = title + date_time
        # 创建md5对象
        hl = hashlib.md5()
        hl.update(news_str.encode(encoding='utf-8'))
        news_md5 = hl.hexdigest()
        item['title'] = title
        item['date_time'] = date_time
        item['news_source'] = news_source
        item['news_body'] = news_body
        item['news_md5'] = news_md5

        return item