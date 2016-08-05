#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import json
import sys
import time


class Utils(object):
    @staticmethod
    def json_loads(raw):
        return json.loads(raw, encoding="UTF-8")

    @staticmethod
    def json_dumps(raw):
        return json.dumps(raw, indent=None, encoding="UTF-8", ensure_ascii=False)

    @staticmethod
    def decode_str_to_time(time_str):
        try:
            time_array = time.strptime(time_str, "%Y%m%d")
            timestamp = int(time.mktime(time_array))
            return timestamp
        except Exception as e:
            # Utils.print_log(u'解码时间戳字符串错误: %s' % e)
            sys.exit(1)
