.. _intro-overview:

====
概览
====

截图展示
========

共分两部分，分别为 Web 端的站点管理后台，以及 Kindle 设备端的书籍显示效果

Web
---

.. image:: images/web/0-index.png
   :scale: 25 %
.. image:: images/web/1-subscription.png
   :scale: 25 %
.. image:: images/web/2-deliver-log.png
   :scale: 25 %
.. image:: images/web/3-password-change.png
   :scale: 25 %
.. image:: images/web/4-invitations.png
   :scale: 25 %

Kindle
------

.. image:: images/kindle/0-books.png
   :scale: 21 %
.. image:: images/kindle/1-book-toc1.png
   :scale: 21 %

.. image:: images/kindle/2-book-toc2.png
   :scale: 21 %
.. image:: images/kindle/3-book-toc3.png
   :scale: 21 %
.. image:: images/kindle/4-book-toc4.png
   :scale: 21 %

.. image:: images/kindle/5-post1.png
   :scale: 21 %
.. image:: images/kindle/6-post2.png
   :scale: 21 %


部署说明
========


系统设计
========

.. mermaid::
   :caption: 系统架构设计图
   :align: center

   graph TB
        MoEar -->|发送任务| Celery((Celery))
        Celery -->|抓取任务<定时>| spider[moear.spider]
        Celery -->|打包任务| package[moear.package]
        Celery -->|投递任务| deliver
        subgraph 邮件系统
        deliver
        end
        subgraph stevedore
            spider
            package
        end
        subgraph moear-api-common
            zhihu[moear-spider-zhihudaily]
            mobi[moear-package-mobi]
        end
        spider -->|爬虫插件| zhihu
        package -->|打包插件| mobi

        click MoEar "http://moear.rtfd.io"
        click Celery "http://docs.celeryproject.org"
        click spider "http://moear-api-common.rtfd.io"
        click package "http://moear-api-common.rtfd.io"
        click zhihu "http://moear-spider-zhihudaily.rtfd.io" "知乎日报"
        click mobi "http://moear-package-mobi.rtfd.io" "mobi"

.. hint::

    抓取与打包功能均以插件形式实现，便于扩展和替换，投递系统由于比较固定，于是实现在了主服务中。

.. todo::

    关于投递系统，为实现节省流量的目的，实现时做了合并投递，即多人订阅了同一个文章源，
    会在该文章当日爬取后合并为一封邮件，加入多个收件地址的形式进行投递。小规模情况下测试正常，
    没有问题，但作者在网上(非官网)看到了一些 Kindle 的投递限制，由于不便测试，故先记录在下:

    #. 一份邮件超过15个不同的【发送至Kindle】电子邮箱，会被认定为垃圾邮件而被Amazon拒绝接收
    #. 附加大于50MB会投递失败

    以上两点未经确认，故暂不为其做应对处理

    其实第二点是可以测试的，但一般情况下应该遇不到这么大的文章，而且吧。懒。。懒。。。（溜了

模型设计
========

.. hint:: 下图为 ``SVG`` 的矢量图，点击可放大查看

.. image:: images/db/er_diagram.svg
   :scale: 100 %

.. hint:: 具体数据模型字段信息，可查看相应应用 ``models`` 中的定义，此处不再赘述

.. note::

    从模型 ER 图中您也可以看出，原本设计的功能很多，但考虑到开发周期，目前只实现了最核心的功能。
    关于文章管理、分类系统等，会在之后版本中陆续实现，但愿不会烂尾（羞~
