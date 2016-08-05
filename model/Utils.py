#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import json


class Utils(object):
    @staticmethod
    def json_loads(raw):
        return json.loads(raw, encoding="UTF-8")

    @staticmethod
    def json_dumps(raw):
        return json.dumps(raw, indent=None, encoding="UTF-8", ensure_ascii=False)