# -*- coding: utf-8 -*-
import scrapy
import hashlib
import configparser
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

        # self.get_tyc_cookies()
        # url = "https://www.tianyancha.com/company/22822"  # 北京百度网讯科技有限公司
        # yield scrapy.Request(url, headers=self.headers, cookies=self.cookies)
        # yield scrapy.Request(self.start_urls[0], headers=self.headers, cookies=self.cookies)

    def parse(self, response):
        keys_list = response.meta
        print(keys_list["category"])
        print(keys_list["url"])
        # for keys in response.meta.keys():
        #     print(keys)

        # node_list = response.xpath("//div[@id='headLineDefault']")
        #
        # for node in node_list:
        #     href = node.xpath(".//li/a/@href").extract()
        #     print(href)
        #     # title = node.xpath("./h2/a/text()").extract()
        #
        #     # 判断返回的href是否为空，如果不为空，则需要获取内容
        #     for href_str in href:
        #         if len(href_str.strip()) > 0:
        #             yield scrapy.Request(href_str.strip(), callback=self.parse_details)

    def parse_details(self, response):
        # 验证这个class的标题是否存在，如果不存在，则使用其它的方法查找
        title_1 = response.xpath("//div[@class='yc_tit']/h1/text()").extract()
        parsed_return = ''
        if title_1 != '':
            parsed_return = self.parse_title_1(response)
        else:
            # 解析另一个class
            self.parse_title_2(response)
        yield parsed_return

    def parse_title_1(self, response):
        item = NewsCrawlingSystemItem()
        print("2")
        title = response.xpath("//div[@class='yc_tit']/h1/text()").extract()[0].strip()
        date_time = response.xpath("//div[@class='yc_tit']/p/span/text()").extract()[0].strip()
        news_source = response.xpath("//div[@class='yc_tit']/p/a/text()").extract()[0].strip()
        news_body_arr = response.xpath("//div[@class='yc_con_txt']//p/text()").extract()
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

    def parse_title_2(self, response):
        item = NewsCrawlingSystemItem()
        node_list = response.xpath("//div[@id='artical']")

        for node in node_list:
            artical_title = node.xpath("./h1/text()").extract()
            # artical_body = node.xpath("//div[@id='main_content']/p[not(@class)]/text()").extract()
            artical_body_node_list = node.xpath("//div[@id='main_content']/p[not(@class)]")

            artical_body = ''
            for body_node in artical_body_node_list:
                raw_body = body_node.extract()
                # new_body = BeautifulSoup(raw_body)
                artical_body += raw_body + "<br>"  # pass

            item['artical_title'] = artical_title[0]
            item['artical_body'] = artical_body
            # item['domain'] = self.allowed_domains[0]

            yield item