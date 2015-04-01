#-*- coding:utf-8 -*-
__author__ = 'haoyuewen'

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

# 设置系统默认编码, 默认为 ascii
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time

# 创建一只蜘蛛爬虫
class BuickSpider(CrawlSpider):
    # 蜘蛛爬虫的唯一标识名
    name = 'buick'
    # 允许爬取的域名
    allow_domains = ['club.autohome.com.cn']
    # 开始爬取的 URL 链接
    start_urls = ["http://club.autohome.com.cn/bbs/forum-c-166-1.html"]
    # 递归爬取的 URL 规则, 爬虫会自动在当前页面中寻找所有符合正则匹配的链接地址, 并进行递归爬去, 需要指定 callback 函数(如何来处理爬取到的页面)
    rules = (
        Rule(SgmlLinkExtractor(allow=('http://club.autohome.com.cn/bbs/thread-.*\.html')), callback="parse_item"),
    )

    # 爬取内容的业务逻辑,
    # 注意, 不要覆盖默认的 parse, 不然会导致父类的框架方法[parse]被覆盖, 它定义了如何执行 Rule 规则下的callback,
    # 会导致 Rule 规则定义的链接内容无法被爬取
    def parse_item(self, response):
        # 论坛文章的标题, 采用 css 选择器的规则
        title = response.css('div#cont_main div#maxwrap-maintopic div#consnav span:last-child::text').extract()[0]
        # 论坛文章的内容 (HTML 代码), , 采用 css 选择器的规则
        contents = response.css('div#cont_main div#maxwrap-maintopic div#F0 div.conright div.rconten div.conttxt div.w740 *').extract()

        print '=============================== Gold Line ================================'
        print '文章标题 ==> ', title
        print '文章主题内容 ==>'
        for c in contents:
            print c
        print '=============================== Gold Line ================================'

        # 方便观察测试的输出内容
        time.sleep(3.8)

