#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>


class ReturnCodeModel(object):
    Code_Success = 200  # 成功
    Code_Expectation_Failed = 417  # 未满足期望值
    Code_Bad_Database_Process = 400  # 错误的数据库操作
    Code_Duplicate = 1062  # 主键重复

    def __init__(self, code=200, msg=u'success', detail=u'', obj=None):
        self.code = code
        self.msg = msg
        self.detail = detail
        self.obj = obj

    def __str__(self):
        out = u'[%d] msg => %s' % (self.code, self.msg)
        if self.detail != u'':
            out += u' | detail => %s' % self.detail
        return out

    def is_success(self, success=None):
        if success is None:
            success = (self.Code_Success,)
        return self.code in success

    def unpack(self):
        rc = {'code': self.code, 'msg': self.msg}
        if self.detail != u'':
            rc['detail'] = self.detail
        return rc

    def pack(self, data=None):
        if data is None:
            data = {}
        if data.has_key('code'):
            self.code = data['code']
        if data.has_key('msg'):
            self.msg = data['msg']
        if data.has_key('detail'):
            self.detail = data['detail']
        else:
            self.detail = u''
        return self
