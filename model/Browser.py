#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import os

from selenium import webdriver


class Browser(object):
    def __init__(self):
        self.driver = None
        self.download_abs_path = './archive'

    def __init_webdriver(self, date_str=None):
        # 实例化一个火狐配置文件
        fp = webdriver.FirefoxProfile()
        # 设置各项参数，参数可以通过在浏览器地址栏中输入about:config查看。

        # 设置成0代表下载到浏览器默认下载路径；设置成2则可以保存到指定目录
        fp.set_preference("browser.download.folderList", 2)

        # 是否显示开始,(个人实验，不管设成True还是False，都不显示开始，直接下载)
        fp.set_preference("browser.download.manager.showWhenStarting", False)

        # 下载到指定目录
        download_abs_path = self.download_abs_path
        if date_str is not None:
            download_abs_path += u'/%s' % date_str
        if not os.path.exists(download_abs_path):
            os.mkdir(download_abs_path)
        fp.set_preference("browser.download.dir", download_abs_path)

        # 不询问下载路径；后面的参数为要下载页面的Content-type的值
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")

        # 禁止PDF预览, 直接下载
        fp.set_preference("pdfjs.disabled", True)

        # 启动一个火狐浏览器进程，以刚才的浏览器参数
        self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.implicitly_wait(5)
