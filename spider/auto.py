#!/usr/bin/env python3
import datetime
import os
import sys

"""
次脚本用来批量执行爬取操作，指定开始&结束日期
"""

formater = '%Y%m%d'
date_begin = datetime.datetime.strptime('20161101', formater)
date_end = datetime.datetime.strptime('20161111', formater)
date_current = date_begin
print('开始日期：{}\n结束日期：{}'.format(date_begin.strftime(formater), date_end.strftime(formater)))

if date_begin > date_end:
    print('Error: 起始日期晚于结束日期！')
    sys.exit(1)

while date_current <= date_end:
    result = os.popen('scrapy crawl zhihu_daily -a date={} -a force=True'.format(date_current.strftime(formater)))
    for line in result:
        print(line)
    date_current += datetime.timedelta(days=1)
