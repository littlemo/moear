.. _topics-plugin:

========
插件开发
========

为保证足够的松耦合设计，本项目采用了基于 `stevedore`_ 的扩展插件实现方式。
现支持两种插件，``entry_points`` 列出如下:

#. 爬虫插件： ``moear.spider``
#. 打包插件： ``moear.package``

两种插件均提供了默认参考实现，下面分章节进行简要说明


.. _stevedore: https://docs.openstack.org/stevedore/latest/
