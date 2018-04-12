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
.. image:: images/web/1-subscription.png
.. image:: images/web/2-deliver-log.png
.. image:: images/web/3-password-change.png
.. image:: images/web/4-invitations.png

Kindle
------

.. image:: images/kindle/0-books.png
.. image:: images/kindle/1-book-toc1.png
.. image:: images/kindle/2-book-toc2.png
.. image:: images/kindle/3-book-toc3.png
.. image:: images/kindle/4-book-toc4.png
.. image:: images/kindle/5-post1.png
.. image:: images/kindle/6-post2.png


部署说明
========


架构设计
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


模型设计
========

.. hint:: 下图为 ``SVG`` 的矢量图，可右键 **在新标签页中打开图片** ，以便放大查看

.. image:: images/db/er_diagram.svg

.. hint:: 具体数据模型字段信息，可查看相应应用 ``models`` 中的定义，此处不再赘述
