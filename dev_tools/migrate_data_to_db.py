#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

# 此脚本为将 `V1.0.0` 版本中已爬取的数据文件填充入Django相应数据表中
# 使用方法：将从MySQL导出的article表 `.sql` 文件，放入 `./data` 路径下

import logging
import os
import re

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(name)s][%(filename)s:%(lineno)d][%(levelname)s] %(message)s')
logger = logging.getLogger('Tool')

_matches = lambda l, r: any([r.search(l)])
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
METADATA_RE = re.compile(r'^\(.*\);|,$')


def yield_item_data(sql_file_path):
    sql = os.path.abspath(sql_file_path)
    logger.info('sql文件路径: {}'.format(sql))

    # 验证传入路径文件是否存在
    if not os.path.exists(sql):
        return None

    # 读取文件并通过Re获取到所有待处理数据条
    with open(sql, 'r') as s:
        cnt_record = 0
        lines = s.readlines()
        for l in lines:
            if _matches(l, METADATA_RE):
                cnt_record += 1
                l = l.strip()
                logger.debug(l)
                # TODO 此处使用一个数据模型格式化条目数据，并进行插入DB的操作
        logger.info('共处理记录条目：{}'.format(cnt_record))


print(yield_item_data(os.path.join(BASE_DIR, 'data/article.sql')))
