#-*- coding:utf-8 -*-
__author__ = 'haoyuewen'

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from autohome_bbs_buick.items import AutohomeBbsBuickItem
from time import strptime

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
    # start_urls = ["http://club.autohome.com.cn/bbs/forum-c-166-1.html"]
    start_urls = ["http://club.autohome.com.cn/bbs/thread-c-166-27964580-1.html"]
    # 递归爬取的 URL 规则, 爬虫会自动在当前页面中寻找所有符合正则匹配的链接地址, 并进行递归爬去, 需要指定 callback 函数(如何来处理爬取到的页面)
    rules = (
        Rule(SgmlLinkExtractor(allow=('http://club.autohome.com.cn/bbs/thread-.*\.html')), callback="parse_item"),
    )

    # 爬取内容的业务逻辑,
    # 注意, 不要覆盖默认的 parse, 不然会导致父类的框架方法[parse]被覆盖, 它定义了如何执行 Rule 规则下的callback,
    # 会导致 Rule 规则定义的链接内容无法被爬取
    def parse_item(self, response):

        items = []

        # 采用 css 选择器的规则
        # 论坛主题内容 DOM 父元素
        maintopic_dom = response.css('div#cont_main div#maxwrap-maintopic')

        # 论坛文章的标题
        title_arr = maintopic_dom.css('div#consnav span:last-child::text').extract()
        title = title_arr[0] if title_arr else ''
        # 文章内容 DOM 父元素
        contstxt_dom = maintopic_dom.css('div.contstxt')

        # 文章发表时间
        pubtime_arr = contstxt_dom.css('div.conright div.rtopcon span[xname=date]::text').extract()
        pubtime = pubtime_arr[0] if pubtime_arr else ''

        # 论坛文章的内容 (HTML 代码), , 采用 css 选择器的规则
        contents = contstxt_dom.css('div.conright div.rconten div.conttxt div.w740 *::text').extract()

        # 文章作者 和 个人主页
        author_a_dom = maintopic_dom.css('div.conleft ul.maxw li.txtcenter a.c01439a')
        author_arr = author_a_dom.css('::text').extract()
        author = author_arr[0] if author_arr else ''
        author_url_arr = author_a_dom.css('::attr(href)').extract()
        author_url = author_url_arr[0] if author_url_arr else ''

        # 作者注册时间
        reg_time_arr = maintopic_dom.css('div.conleft ul.leftlist li:nth-child(5)::text').extract()
        reg_time = reg_time_arr[0] if reg_time_arr else ''
        reg_time = reg_time[3:] if reg_time else ''
        # 作者所在地
        addr_arr = maintopic_dom.css('div.conleft ul.leftlist li:nth-child(6) a.c01439a::text').extract()
        addr = addr_arr[0] if addr_arr else ''
        # 作者关注车型
        attent_vehicle_arr = maintopic_dom.css('div.conleft ul.leftlist li:nth-child(7) a.c01439a::text').extract()
        attent_vehicle = attent_vehicle_arr[0] if attent_vehicle_arr else ''


        print '=============================== Gold Line ================================'
        print '文章标题 ==> ', title
        print '发表时间 ==>', pubtime
        print '作者 ==> ', author
        print '个人主页 ==> ', author_url
        print '注册时间 ==> ', reg_time
        print '所在地 ==> ', addr
        print '关注车型 ==> ', attent_vehicle
        print '文章主题内容 ==>'


        content = ''
        for c in contents:
            if c.strip():
                print c
                content = content + c + '\n'

        topic_item = AutohomeBbsBuickItem()
        topic_item['title'] = title
        topic_item['content'] = content
        topic_item['pub_time'] = pubtime
        topic_item['author'] = author
        topic_item['author_url'] = author_url
        topic_item['reg_time'] = reg_time
        topic_item['addr'] = addr
        topic_item['attent_vehicle'] = attent_vehicle

        items.append(topic_item)

        ## 论坛文章回复的内容 ##
        reply_doms = response.css('div#cont_main div#maxwrap-reply div.contstxt')

        for reply_dom in reply_doms:

            reply_pub_time = reply_dom.css('div.conright div.rtopconnext span[xname=date]::text').extract()[0]

            reply_author_a_dom = reply_dom.css('div.conleft ul.maxw li.txtcenter a.c01439a')

            reply_author = reply_author_a_dom.css('::text').extract()[0]

            reply_author_url = reply_author_a_dom.css('::attr(href)').extract()[0]

            # 作者注册时间
            reply_reg_time = reply_dom.css('div.conleft ul.leftlist li:nth-child(5)::text').extract()[0]
            reply_reg_time = reply_reg_time[3:] if reply_reg_time else ''

            # 作者所在地
            reply_addr = reply_dom.css('div.conleft ul.leftlist li:nth-child(6) a.c01439a::text').extract()[0]

            # 作者关注车型
            reply_attent_vehicle_arr = reply_dom.css('div.conleft ul.leftlist li:nth-child(7) a.c01439a::text').extract()
            reply_attent_vehicle = reply_attent_vehicle_arr[0] if reply_attent_vehicle_arr else ''

            reply_contents_dom = reply_dom.css('div.conright div.rconten div.x-reply div.w740')
            reply_contents = []
            if (reply_contents_dom.css('div.yy_reply_cont')):
                reply_contents = reply_contents_dom.css('div.yy_reply_cont *::text').extract()
            else:
                reply_contents = reply_contents_dom.css('*::text').extract()

            print '回复人 ==> ', reply_author
            print '发表时间 ==>', reply_pub_time
            print '回复人主页 ==> ', reply_author_url
            print '回复人注册时间 ==> ', reply_reg_time
            print '回复人所在地 ==> ', reply_addr
            print '回复人关注车型 ==> ', reply_attent_vehicle
            print '回复内容 ==>'

            reply_content = ''
            for c in reply_contents:
                if c.strip():
                    print c
                    reply_content = reply_content + c + '\n'


            reply_item = AutohomeBbsBuickItem()
            reply_item['title'] = ''
            reply_item['content'] = reply_content
            reply_item['pub_time'] = reply_pub_time
            reply_item['author'] = reply_author
            reply_item['author_url'] = reply_author_url
            reply_item['reg_time'] = reply_reg_time
            reply_item['addr'] = reply_addr
            reply_item['attent_vehicle'] = reply_attent_vehicle

            items.append(reply_item)

        # 方便观察测试的输出内容
        print '=============================== Gold Line ================================'

        return items



