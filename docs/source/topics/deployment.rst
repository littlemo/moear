.. _topics-deployment:

========
高级部署
========

除了 :ref:`intro-overview-deployment` 中描述的基础部署，为了更靠的监控 ``Celery``
异步消息队列的运行情况，您可以额外部署一个监控容器 `docker-celery-flower`_ 。

在已有的 ``docker-compose.yml`` 文件中增加内容如下::

    version: '2'
    services:
      flower:
        image: littlemo/docker-celery-flower
        container_name: moear-flower
        hostname: moear-flower
        restart: unless-stopped
        mem_limit: 1G
        ports:
          - "8889:5555"
        networks:
          - frontend
          - backend
        volumes:
          - ./volumes/runtime/flower:/app/runtime:rw
        environment:
          - CELERY_BROKER_URL=redis://moear-redis:6379/0
          - FLOWER_BASIC_AUTH=用户名:密码
          - FLOWER_PERSISTENT=True
        depends_on:
          - redis
          - moear

.. attention::

    前两行语句主要为了让您清楚层级，从第三行开始将容器配置添加到 ``docker-compose.yml`` 中即可

.. attention::

    环境变量中的 ``FLOWER_BASIC_AUTH`` 需要您替换为您的账户验证信息。

重新执行 ``docker-compose up -d`` 命令完成容器构建，部署完成后，您可以通过浏览器访问（
``http://127.0.0.1:8889`` ）来查看 ``Celery`` 的运行状况


.. _docker-celery-flower: https://github.com/littlemo/docker-celery-flower
