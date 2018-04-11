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

另外我还实现了系统默认安装的文章源，知乎日报，已开源到 GitHub 上，可为您开发文章源插件提供参考
`moear-spider-zhihudaily`_

.. hint::

    作为提供文章来源的插件，欢迎有能力的小伙伴儿实现自己喜欢的文章源爬虫插件，
    如果您这样做了请联系我将其加入官方插件列表，让大家看到您的贡献

插件列表
--------

#. `知乎日报`_

打包插件
========

打包插件作为书籍文件的生成者，主要责任为将传入的文章数据结构处理后，本地化文章中的图片，
同时对文件进行压缩、灰度化等操作，最终打包生成书籍文件字节串返回给调用者。

具体协议与接口定义，可参考 `moear-api-common`_

另外我事先了系统默认安装的打包工具，mobi打包，已开源道 Github 上，可为您开发打包插件提供参考
`moear-package-mobi`_

.. note::

    该 mobi 打包工具为基于 Amazon 官方打包工具 `KindleGen`_ 的实现。

.. hint::

    一般情况来说该插件已经足够完善，除非需要支持新的书籍格式，否则不需要实现额外的打包插件

插件列表
--------

#. `mobi`_


.. _stevedore: https://docs.openstack.org/stevedore/latest/
.. _moear-api-common: http://moear-api-common.rtfd.io
.. _moear-spider-zhihudaily: http://moear-spider-zhihudaily.rtfd.io
.. _知乎日报: https://github.com/littlemo/moear-spider-zhihudaily
.. _moear-package-mobi: http://moear-package-mobi.rtfd.io
.. _mobi: https://github.com/littlemo/moear-package-mobi
.. _KindleGen: https://www.amazon.com/gp/feature.html?docId=1000765211
