.. _topics-plugin:

========
插件开发
========

为保证足够的松耦合设计，本项目采用了基于 `stevedore`_ 的扩展插件实现方式。
现支持两种插件，``entry_points`` 列出如下:

#. 爬虫插件： ``moear.spider``
#. 打包插件： ``moear.package``

两种插件均提供了默认参考实现，下面分章节进行简要说明

爬虫插件
========

爬虫插件作为文章来源的提供者，主要责任为抓取某一特定文章源中的文章数据，并返回规定的数据结构。

具体协议与接口定义，可参考 `moear-api-common`_

另外我还实现了系统默认安装的文章源，知乎日报，也已开源到 GitHub 上，可为您开发文章源插件参考
`moear-spider-zhihudaily`_


.. _stevedore: https://docs.openstack.org/stevedore/latest/
.. _moear-api-common: http://moear-api-common.rtfd.io
.. _moear-spider-zhihudaily: http://moear-spider-zhihudaily.rtfd.io
