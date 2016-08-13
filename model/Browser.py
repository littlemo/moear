#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import codecs
import os
import sys

import requests
from selenium import webdriver

from Utils import Utils


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
        if self.driver is not None:
            self.driver.quit()
        self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.implicitly_wait(5)

    @staticmethod
    def __get_article_info_by_id(aid):
        headers = {'Host': 'news-at.zhihu.com',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) '
                                 'AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
        request_url = u'http://news-at.zhihu.com/api/4/news/%s' % aid
        news = requests.get(request_url, headers=headers)
        # print news.url, news.status_code
        # print news.text
        if news.status_code != 200:
            Utils.print_log(u'获取指定文章信息失败: [%s]%s' % (news.status_code, news.text), prefix=u'[请求文章信息]')
            sys.exit(1)
        return news.text

    def save_web_with_articles(self, articles):
        for a in articles:
            article_info = Utils.json_loads(self.__get_article_info_by_id(a.article_id))
            path = u'%s/%s' % (self.download_abs_path, Utils.encode_time_to_str(a.timestamp))
            if not os.path.exists(path):
                os.mkdir(path)
            output = u'%s/%s.html' % (path, a.title)
            fd = codecs.open(output, 'w', 'utf-8')
            fd.write(article_info['body'])
            fd.flush()
            fd.close()
