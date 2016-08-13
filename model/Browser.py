#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import codecs
import os
import sys

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from Utils import Utils


class Browser(object):
    headers = {'Host': 'news-at.zhihu.com',
               'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) '
                             'AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}

    def __init__(self, path=None):
        self.driver = None
        self.download_abs_path = './archive' if path is None else path

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
            base_path = u'%s/%s' % (self.download_abs_path, Utils.encode_time_to_str(a.timestamp))
            if not os.path.exists(base_path):
                os.mkdir(base_path)

            # 创建图片资源存放路径
            img_path = u'%s/%s' % (base_path, u'img')
            if not os.path.exists(img_path):
                os.mkdir(img_path)

            body = article_info['body']
            soup = BeautifulSoup(body, "lxml")
            img_list = soup.find_all('img')
            for i in img_list:
                img_link = i.get('src')
                img_name = img_link.split('/')[-1]
                if u'equation?tex=' in img_name or u'.' not in img_name:
                    Utils.print_log(u'遇到无法识别的img: %s' % img_link, prefix=u'[本地化图片资源]')
                    break
                img_rsp = requests.get(img_link, stream=True)
                img_content = img_rsp.content
                try:
                    with open(u'%s/%s' % (img_path, img_name), 'wb') as img:
                        img.write(img_content)
                except Exception as e:
                    Utils.print_log(u'保存图片异常: %s' % e, prefix=u'[保存图片资源]')
                    sys.exit(1)
                i['src'] = u'img/' + img_name

            body = soup.prettify(encoding='utf8')

            # 保存页面
            title = a.title.replace('/', '|')
            output = u'%s/%s.html' % (base_path, title)
            # Utils.print_log(u'路径名: %s' % output)
            Utils.print_log(a)
            fd = codecs.open(output, 'w', 'utf-8')
            fd.write(body)
            fd.flush()
            fd.close()

        Utils.print_log(u'共保存%d篇文章' % len(articles), prefix=u'[保存文章列表]')
