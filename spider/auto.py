#!/usr/bin/env python3
import argparse
import datetime
import os
import sys

"""
次脚本用来批量执行爬取操作，指定开始&结束日期
"""

des = u'''例子:
    ./auto.py 20161029 20161101  # 抓取[20161029, 20161101)的文章
    '''
parser = argparse.ArgumentParser(prog=u'auto.py',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=des)
parser.add_argument("begin", help=u"开始日期(包含)，格式yyyymmdd")
parser.add_argument("end", help=u"结束日期(不含)，格式yyyymmdd")

args = parser.parse_args()
begin = args.begin
end = args.end

formater = '%Y%m%d'
try:
    date_begin = datetime.datetime.strptime(begin, formater)
    date_end = datetime.datetime.strptime(end, formater)
except ValueError as e:
    print('日期格式错误(yyyymmdd): {}'.format(e))
    sys.exit(1)
date_current = date_begin
print('开始日期：{}\n结束日期：{}'.format(date_begin.strftime(formater), date_end.strftime(formater)))

if date_begin > date_end:
    print('Error: 起始日期晚于结束日期！')
    sys.exit(1)

log_file = ' --logfile {}.log'.format(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 'log', datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')))

while date_current < date_end:
    result = os.popen('scrapy crawl zhihu_daily -a date={} -a force=True{}'
                      .format(date_current.strftime(formater), log_file))
    for line in result:
        print(line)
    date_current += datetime.timedelta(days=1)
