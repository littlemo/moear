FROM python:3.5

# 定义构建时元数据
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION
LABEL maintainer="moore@moorehy.com" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="MoEar" \
      org.label-schema.description="貘耳朵文章抓取与推送服务" \
      org.label-schema.url="https://hub.docker.com/r/littlemo/MoEar/" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/littlemo/MoEar" \
      org.label-schema.vendor="littlemo" \
      org.label-schema.version=$VERSION \
      org.label-schema.schema-version="1.0"

# 设置用户
USER root

# 替换为中科大软件源
RUN sed -i 's|deb.debian.org|mirrors.ustc.edu.cn|g' /etc/apt/sources.list && \
    sed -i 's|security.debian.org|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list

# 安装mysqlclient库&nginx
RUN apt-get update --fix-missing && apt-get install -y \
        libmysqlclient-dev libssl-dev \
        nginx gettext \
        --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 添加Python软件包需求文件
RUN mkdir -p /app/requirements
ADD ./requirements /app/requirements

# 安装Python相关Packages
WORKDIR /app
RUN pip install requirements/wheels/*.whl
RUN pip install --no-cache-dir -r requirements/pip.txt

# 删除镜像初始化用的文件，并创建用于挂载的路径
RUN rm -rf * && \
    mkdir -p /app/run && \
    mkdir -p /app/server && \
    mkdir -p /app/runtime/log/nginx

# 开放对外端口
EXPOSE 80 443

# 添加Server源码文件
ADD ./server /app/server

# 添加启动脚本文件
ADD ./docker/scripts/*.sh /app/run/
RUN chmod a+x /app/run/*.sh

# Volumes 挂载点配置
VOLUME ["/app", "/etc/nginx"]

WORKDIR /app/server
ENTRYPOINT ["/app/run/start.sh"]
CMD ["gunicorn", "-w 3", "-b 127.0.0.1:8000", "server.wsgi"]
