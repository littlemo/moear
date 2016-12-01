# 声明

以下知乎日报协议分析主要参考于 [知乎日报 API 分析](https://github.com/izzyleung/ZhihuDailyPurify/wiki/知乎日报-API-分析) ，针对于部分协议进行了额外的验证和补充，以及实际爬取的逻辑阐述，侵删

> 感谢 `Xiao Liang` 前辈的贡献 Orz，正愁无门路打算直接硬抓Web版文章信息的时候，看到您的这篇分析文章，如醍醐灌顶一般，整个人瞬间精神了！

# API 说明
* 本协议分析主要针对于知乎日报第 __4__ 版 API，且主要关注于文章相关内容获取部分，其余更全面的部分，如：启动界面、软件版本、评论相关、主题日报等 APP 相关协议可参考上述链接

* 以下所有 API 使用的 HTTP Method 均为 `GET`

# API 分析

### 1. 最新消息
* URL: __GET__ `http://news-at.zhihu.com/api/4/news/latest`  
* 响应实例：

```json
{
    "date": "20161201",
    "stories": [{
        "images": ["http://pic1.zhimg.com/1336c8a5e842c11912014f093cc69d58.jpg"],
        "type": 0,
        "id": 9026396,
        "ga_prefix": "120111",
        "title": "收了的税全部返还，民众福利怎么就大大下降了？"
    }
    ...
    ],
    "top_stories": [{
        "image": "http://pic4.zhimg.com/8fc4831c28432f700b6400de882fd833.jpg",
        "type": 0,
        "id": 9022827,
        "ga_prefix": "120113",
        "title": "爱看《冰与火之歌》和《魔戒》，没想到背后这么多八卦"
    },
    ...
    ]
}
```

* 分析：
    * `date` : 日期
    * `stories` : 当日新闻
        * `title` : 新闻标题
        * `images` : 图像地址（官方 API 使用数组形式。目前暂未有使用多张图片的情形出现，__曾见无__ `images` __属性的情况__，请在使用中注意 ）
        * `ga_prefix` : 供 Google Analytics 使用
        * `type` : 作用未知
        * `id` : `url` 与 `share_url` 中最后的数字（应为内容的 id）
        * `multipic` : 消息是否包含多张图片（仅出现在包含多图的新闻中）
    * `top_stories` : 界面顶部 ViewPager 滚动显示的显示内容（子项格式同上）（请注意区分此处的 `image` 属性与 `stories` 中的 `images` 属性）

* 补充：
    - `images` 字段不存在的情况，如：[8 月 1 日，这些新闻值得你了解一下](http://daily.zhihu.com/story/4065555)，获取到的列表项内容为：

    ```json
    {
        "type": 0,
        "id": 4065555,
        "ga_prefix": "010115",
        "title": "8 月 1 日，这些新闻值得你了解一下"
    }
    ```

    - `top_stories`.`image` 字段中的图片为APP中的顶部轮播图使用，故分辨率会比 `stories` 中的相同文章块 `images` 里的图片拥有更高的分辨率，一般情况下，前者为 `640*640`，而后者仅为 `150*150`。故在做文章爬取时可以根据实际需求进行选择，下节将说明如何获取非热文的高质量封面图

### 2. 消息内容获取与离线下载
* URL: `http://news-at.zhihu.com/api/4/news/9026396`  
* 使用在 `最新消息` 中获得的 `id`，拼接在 `http://news-at.zhihu.com/api/4/news/` 后，得到对应消息 JSON 格式的内容
* 响应实例：

```json
{
    "body": "...页面具体内容的html部分...",
    "image_source": "韦你好 / 知乎",
    "title": "瞎扯 · 如何正确地吐槽",
    "image": "http://pic3.zhimg.com/ab8cb35b812c249dff4cfd8cd5bd1056.jpg",
    "share_url": "http://daily.zhihu.com/story/9024081",
    "js": [],
    "ga_prefix": "120106",
    "section": {
        "thumbnail": "http://pic3.zhimg.com/9c7eebeb525f7f9135fd961080b80a2e.jpg",
        "id": 2,
        "name": "瞎扯"
    },
    "images": ["http://pic3.zhimg.com/9c7eebeb525f7f9135fd961080b80a2e.jpg"],
    "type": 0,
    "id": 9024081,
    "css": ["http://news-at.zhihu.com/css/news_qa.auto.css?v=4b3e3"]
}
```

* 分析：
    * `body` : HTML 格式的新闻
    * `image-source` : 图片的内容提供方。为了避免被起诉非法使用图片，在显示图片时最好附上其版权信息。
    * `title` : 新闻标题
    * `image` : 获得的图片同 `最新消息` 获得的图片分辨率不同。这里获得的是在文章浏览界面中使用的大图。
    * `share_url` : 供在线查看内容与分享至 SNS 用的 URL
    * `js` : 供手机端的 WebView(UIWebView) 使用
    * `recommenders` : 这篇文章的推荐者
    * `ga_prefix` : 供 Google Analytics 使用
    * `section` : 栏目的信息
        * `thumbnail` : 栏目的缩略图
        * `id` : 该栏目的 `id`
        * `name` : 该栏目的名称
    * `type` : 新闻的类型
    * `id` : 新闻的 id
    * `css` : 供手机端的 WebView(UIWebView) 使用
        * 可知，知乎日报的文章浏览界面利用 WebView(UIWebView) 实现

* __特别注意__  
    在较为特殊的情况下，知乎日报可能将某个主题日报的站外文章推送至知乎日报首页。  
    响应实例：

```json
{
    "theme_name": "电影日报",
    "title": "五分钟读懂明星的花样昵称：一美、法鲨……",
    "share_url": "http://daily.zhihu.com/story/3942319",
    "js": [],
    "ga_prefix": "052921",
    "editor_name": "邹波",
    "theme_id": 3,
    "type": 1,
    "id": 3942319,
    "css": [
        "http://news.at.zhihu.com/css/news_qa.6.css?v=b390f"
    ]
}
```

    此时返回的 JSON 数据缺少 `body`，`image-source`，`image`，`js` 属性。多出 `theme_name`，`editor_name`，`theme_id` 三个属性。`type` 由 `0` 变为 `1`。

* 补充：
    - 文章爬取时主要使用 `body`(内容)，`image`( __高清封面图__ )，`share_url`(文章url)，`title`(标题)
    - 另外需要对 `type` 进行判断，若为 `1` ，则另行处理
    - `recommenders` 字段非常驻字段，即不一定存在

### 3. 过往消息
* URL: `http://news-at.zhihu.com/api/4/news/before/20131119`  
* __若果需要查询 11 月 18 日的消息，__`before` __后的数字应为__ `20131119`  
* __知乎日报的生日为 2013 年 5 月 19 日，若__ `before` __后数字小于__ `20130520` __，只会接收到空消息__  
* 输入的今日之后的日期仍然获得今日内容，但是格式不同于最新消息的 JSON 格式  
* 响应实例：

```json
{
    "date": "20131118",
    "stories": [{
        "images": ["http://p4.zhimg.com/7b/c8/7bc8ef5947b069513c51e4b9521b5c82.jpg"],
        "type": 0,
        "id": 1747159,
        "ga_prefix": "111822",
        "title": "深夜食堂 · 我的张曼妮"
    },
    ...
    ]
}
```

* 格式与前同，恕不再赘述

* 补充：
    - 使用此接口获取的当日消息是不包含 `top_stories` 字段的，仅含该日 `date` & `stories` 字段
    - 一天的时间差需单独封装处理，通过获取到的文章id，调用上述第二条API即可获取到相应文章的详细信息，如高清封面图等
