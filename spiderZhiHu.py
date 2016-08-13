#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import argparse
import sys

import config
from model.Zhihu import Zhihu

reload(sys)
sys.setdefaultencoding('utf8')

# DONE 1) 实现抓取当天文章, 并存入DB, DB应包含是否已阅读, 是否感兴趣, 是否TOP, 以及相关TAG(此数据阅读后更新)
# TODO 2) 从DB中取出当天的文章, 生成对应的Bookmarks文件(将[TOP], [D]标志表现在文章title中), 用于导入到浏览器
# DONE 3) 将DB中的文章请求并保存到本地
# TODO 4) 将本地保存的文章生成为mobi文件, 并发送到Kindle


zhihu = Zhihu()

cmd_list = ['spider', 'local']
parser = argparse.ArgumentParser()
parser.add_argument("command", choices=cmd_list, help=u"要执行的子命令")
args = parser.parse_args(sys.argv[1:2])

args_child_list = sys.argv[2:]
if args.command == 'spider':
    des = u'''例子:
    ./spdierZhiHu.py spider  # 抓取当日的文章列表, 插入到DB
    ./spdierZhiHu.py spider -s  # 抓取当日的文章列表, 插入到DB, 并将文章保存到本地
    ./spdierZhiHu.py spider -n -s  # 从DB获取当日的文章列表, 并将文章保存到本地
    ./spdierZhiHu.py spider -d 20160809  # 抓取20160809的文章列表, 插入到DB
    ./spdierZhiHu.py spider -d 20160809 -s  # 抓取20160809的文章列表, 插入到DB, 并将文章保存到本地
    ./spdierZhiHu.py spider -d 20160809 -n -s  # 从DB获取20160809的文章列表, 并将文章保存到本地
    '''
    parser_info = argparse.ArgumentParser(prog=u'spiderZhiHu.py %s' % args.command,
                                          formatter_class=argparse.RawDescriptionHelpFormatter,
                                          description=des)
    parser_info.add_argument('-d', '--date', default=None, help=u"指定日期")
    parser_info.add_argument('-s', '--save', action='store_true', help=u"保存文章到本地")
    parser_info.add_argument('-n', '--no_spider', action='store_true', help=u"不抓取文章列表, 从DB获取")
    args_info = parser_info.parse_args(args_child_list)

    if args_info.no_spider:
        zhihu.load_articles_from_db(args_info.date)
    else:
        zhihu.spider_articles_from_net(args_info.date)

    if args_info.save:
        zhihu.spider_articles_html(config.article_archive_abs_path)
    else:
        zhihu.print_articles()
