#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import json
import sys
import time


class Utils(object):
    @staticmethod
    def print_log(log, newline=True, prefix=u''):
        debug = True
        out = u''
        if prefix != u'':
            out = u'%s' % prefix
        if type(log) == list:
            if not newline and len(log) > 0:
                out += u'| '
            if newline and len(log) > 0:
                out += u'\n'
            for item in log:
                if newline:
                    out += u'%s\n' % item.encode('utf8')
                else:
                    out += u'%s | ' % item.encode('utf8')
            if not newline:
                out = out.rstrip()
                out += u'\n'
        elif type(log) in [unicode, str]:
            out += u'%s\n' % log.encode('utf8')
        else:
            out += u'%s\n' % log
        if debug:
            print out,

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
            Utils.print_log(u'解码时间戳字符串错误: %s' % e)
            sys.exit(1)
