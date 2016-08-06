#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Moore.Huang <moore@moorehy.com>

import sys

import requests

from model.Article import Article
from model.Utils import Utils

reload(sys)
sys.setdefaultencoding('utf8')


# TODO 1) 实现抓取当天文章, 并存入DB, DB应包含是否已阅读, 是否感兴趣, 是否TOP, 以及相关TAG(此数据阅读后更新)
# TODO 2) 从DB中取出当天的文章, 生成对应的Bookmarks文件(将[TOP], [D]标志表现在文章title中), 用于导入到浏览器
# TODO 3) 将DB中的文章请求并保存到本地
# TODO 4) 将本地保存的文章生成为mobi文件, 并发送到Kindle


def get_news_by_net():
    headers = {'Host': 'news-at.zhihu.com',
               'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) '
                             'AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
    news = requests.get('http://news-at.zhihu.com/api/4/news/latest', headers=headers)
    # print news.url, news.status_code
    # print news.text
    if news.status_code != 200:
        print(u'获取最新文章列表失败: [%s]%s' % (news.status_code, news.text))
        sys.exit(1)
    return news.text


# content = get_news_by_net()
content = '{"date":"20160804","stories":[{"images":["http:\/\/pic2.zhimg.com\/170f41d397f20d0a4fec647881f40185.jpg"],"type":0,"id":8649054,"ga_prefix":"080422","title":"小事 · 鳄鱼离我七八米"},{"images":["http:\/\/pic1.zhimg.com\/42305a64aa7fda79b7ce4cf701b55418.jpg"],"type":0,"id":8647188,"ga_prefix":"080421","title":"人生还会好吗？这些电影说不会"},{"images":["http:\/\/pic2.zhimg.com\/f5cb73637580d47e9f51c54fe4fcf3e9.jpg"],"type":0,"id":8648821,"ga_prefix":"080420","title":"孩子哭了要不要抱？把尿还是自己尿？来看心理学界怎么说"},{"title":"打算坐火车旅行？问对人了，我有 7 条坐过的线路推荐呢","ga_prefix":"080419","images":["http:\/\/pic2.zhimg.com\/184e276f589c3d118e7cc98de23c2ca1.jpg"],"multipic":true,"type":0,"id":8647901},{"images":["http:\/\/pic1.zhimg.com\/f00450934490548e381aade8227814e4.jpg"],"type":0,"id":8647897,"ga_prefix":"080418","title":"我们玩着游戏慢慢变老，但为什么不接受老年人玩游戏？"},{"images":["http:\/\/pic3.zhimg.com\/c04b5715b7a55d06b0ead498a6bef8d2.jpg"],"type":0,"id":8643769,"ga_prefix":"080417","title":"知乎好问题 · 有哪些经常出现而不易被察觉的洗脑方式？"},{"images":["http:\/\/pic1.zhimg.com\/d7e4e0112b21735d08fd6d11b34bf130.jpg"],"type":0,"id":8647558,"ga_prefix":"080416","title":"用了这种厨房，朋友聚会更开心了"},{"images":["http:\/\/pic2.zhimg.com\/7b72508c891c612254cbf8a8d758f565.jpg"],"type":0,"id":8647268,"ga_prefix":"080415","title":"论文级别的消暑甜品姜撞奶，花十分钟就能做好"},{"title":"想学传统木匠做一些玩意儿，需要的工具并不多","ga_prefix":"080414","images":["http:\/\/pic4.zhimg.com\/3f13ed5f25ed36bb20f6c4d64a25ea3f.jpg"],"multipic":true,"type":0,"id":8641570},{"images":["http:\/\/pic4.zhimg.com\/7ea1749fb6e7666d8c50cb8c3d9e9d73.jpg"],"type":0,"id":8647311,"ga_prefix":"080413","title":"进入管理咨询界和投行前，得先了解哪些硬知识？"},{"images":["http:\/\/pic4.zhimg.com\/14c2d863a5219e1dfb8ef86a5050cf77.jpg"],"type":0,"id":8643379,"ga_prefix":"080412","title":"大误 · 看过金庸写的《阿 Q 八部》吗？"},{"images":["http:\/\/pic2.zhimg.com\/dc6a3a2a361daf98a2ae36492354bd39.jpg"],"type":0,"id":8639660,"ga_prefix":"080411","title":"参加这个超级英雄和美剧迷们的盛会，我也充满了战斗力"},{"images":["http:\/\/pic2.zhimg.com\/d4bbdf8414a23c62ca61ad82bb0090e1.jpg"],"type":0,"id":8644196,"ga_prefix":"080410","title":"卖掉优步中国，Uber 距离 IPO 又近了一大步"},{"images":["http:\/\/pic4.zhimg.com\/b247609f382ec5d097c51d468975fd1b.jpg"],"type":0,"id":8644697,"ga_prefix":"080409","title":"以现有的技术，能不能把地沟油检测出来？"},{"images":["http:\/\/pic4.zhimg.com\/b556013584ac5f190f1a343aad2b75bb.jpg"],"type":0,"id":8645106,"ga_prefix":"080408","title":"写给产品 \/ 市场 \/ 运营的数据抓取黑科技教程"},{"images":["http:\/\/pic2.zhimg.com\/eaf3fb69ddfe636c6c4c40c2c76029c5.jpg"],"type":0,"id":8644252,"ga_prefix":"080407","title":"整点儿奥运 · 这届奥运行不行就看这些了"},{"images":["http:\/\/pic4.zhimg.com\/87f3c53eae92c639ca513072806b3957.jpg"],"type":0,"id":8645033,"ga_prefix":"080407","title":"那些又新又厉害的最新医疗技术，为什么就推广不动呢"},{"images":["http:\/\/pic1.zhimg.com\/dd1487cd8011ec69b3ca45c0faa87bc4.jpg"],"type":0,"id":8643890,"ga_prefix":"080407","title":"软件安装、网站注册的用户协议里有哪些著名的陷阱条款？"},{"images":["http:\/\/pic3.zhimg.com\/032e3bd7ed863e6e7e9b54814ac1612e.jpg"],"type":0,"id":8645359,"ga_prefix":"080407","title":"读读日报 24 小时热门 TOP 5 · 余文乐和「香港贾玲」乌龙绯闻"},{"images":["http:\/\/pic4.zhimg.com\/1ed8efb4152261d238dcde221e23ab8f.jpg"],"type":0,"id":8640199,"ga_prefix":"080406","title":"瞎扯 · 如何正确地吐槽"}],"top_stories":[{"image":"http:\/\/pic4.zhimg.com\/a36b194f626aa66835e0a71d9d84ff67.jpg","type":0,"id":8644252,"ga_prefix":"080407","title":"整点儿奥运 · 这届奥运行不行就看这些了"},{"image":"http:\/\/pic1.zhimg.com\/d43f4df6722e406ed929bbca5c51323c.jpg","type":0,"id":8643769,"ga_prefix":"080417","title":"知乎好问题 · 有哪些经常出现而不易被察觉的洗脑方式？"},{"image":"http:\/\/pic4.zhimg.com\/5aeee37d25d61d9dadb8fc1feab15803.jpg","type":0,"id":8647268,"ga_prefix":"080415","title":"论文级别的消暑甜品姜撞奶，花十分钟就能做好"},{"image":"http:\/\/pic3.zhimg.com\/b5c5fc8e9141cb785ca3b0a1d037a9a2.jpg","type":0,"id":8645359,"ga_prefix":"080407","title":"读读日报 24 小时热门 TOP 5 · 余文乐和「香港贾玲」乌龙绯闻"},{"image":"http:\/\/pic2.zhimg.com\/551fac8833ec0f9e0a142aa2031b9b09.jpg","type":0,"id":8645106,"ga_prefix":"080408","title":"写给产品 \/ 市场 \/ 运营的数据抓取黑科技教程"}]}'

news_content = Utils.json_loads(content)
date = Utils.decode_str_to_time(news_content['date'])
Utils.print_log(u'日期时间戳: <%s>%d' % (news_content['date'], date), prefix=u'[测试]')

# 生成文章列表
articles = []
for a in news_content['stories']:
    article = Article().init_with_time_and_data(date, a)
    articles.append(article)
    # Utils.print_log(article)

# 从文章列表中提取文章ID列表
article_ids = []
for a in articles:
    article_ids.append(a.article_id)

# 若数据包中包含top_stories字段, 则更新文章列表中对象的TOP属性
if 'top_stories' in news_content:
    for top in news_content['top_stories']:
        top_article_id = top['id']
        if top_article_id in article_ids:
            for a in articles:
                if top_article_id == a.article_id:
                    a.top = 1
                    break

# 打印文章列表
for a in articles:
    Utils.print_log(a)
