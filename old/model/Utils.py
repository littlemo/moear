#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import json
import sys
import time
import datetime

import MySQLdb

from model.ReturnCodeModel import ReturnCodeModel


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
                    out += u'%s\n' % item
                else:
                    out += u'%s | ' % item
            if not newline:
                out = out.rstrip()
        elif type(log) in [str]:
            out += u'%s' % log
        else:
            out += u'%s' % log
        if debug:
            print(out)

    @staticmethod
    def process_database(cb, tag, log=True):
        # rcm = ReturnCodeModel(ReturnCodeModel.Code_Bad_Database_Process, u'数据库操作失败')
        try:
            conn = MySQLdb.connect(host='localhost', user='moore', passwd='LittleMO418',
                                   db='mo_zhihu_daily', port=3306, charset='utf8')
            cur = conn.cursor()
            rcm = cb(cur, conn)
            cur.close()
            conn.close()
            if log:
                Utils.print_log(rcm, prefix=u'[%s]' % tag)
            return rcm
        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            rcm = ReturnCodeModel(e.args[0], e.args[1].decode('utf8'))
            Utils.print_log(rcm, prefix=u'[%s]' % tag)
            return rcm

    @staticmethod
    def json_loads(raw):
        return json.loads(raw, encoding="UTF-8")

    @staticmethod
    def json_dumps(raw):
        return json.dumps(raw, indent=None, encoding="UTF-8", ensure_ascii=False)

    @staticmethod
    def encode_time_to_str(timestamp):
        if timestamp is None:
            timestamp = int(time.mktime(datetime.date.today().timetuple()))
        time_array = time.localtime(timestamp)
        other_style_time = time.strftime("%Y-%m-%d", time_array)
        return other_style_time

    @staticmethod
    def decode_str_to_time(time_str, day_offset=0):
        try:
            time_array = time.strptime(time_str, "%Y%m%d")
            timestamp = int(time.mktime(time_array))
            if day_offset != 0:
                timestamp += (int(day_offset) * 24 * 3600)
            return timestamp
        except Exception as e:
            Utils.print_log(u'解码时间戳字符串错误: %s' % e)
            sys.exit(1)