# -*- coding: utf-8 -*-

# Scrapy settings for autohome_bbs_buick project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'autohome_bbs_buick'

SPIDER_MODULES = ['autohome_bbs_buick.spiders']
NEWSPIDER_MODULE = 'autohome_bbs_buick.spiders'

ITEM_PIPELINES = {
    'autohome_bbs_buick.pipelines.AutohomeBbsBuickPipeline': 1,
    'autohome_bbs_buick.pipelines.MySqlStorePipeline': 2,
}

MYSQL_HOST = '192.168.0.210'
MYSQL_DBNAME = 'haoyuewen'
MYSQL_USER = 'haoyuewen'
MYSQL_PASSWD = 'JUFL7Kl5NsPX'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'autohome_bbs_buick (+http://www.yourdomain.com)'
