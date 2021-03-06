#!/usr/bin/env bash

export INSTALL_LOCK_FILE="/app/runtime/install/install.lock"

# 创建install.lock所在路径
install_lock_path=`dirname $INSTALL_LOCK_FILE`
if [ ! -d $install_lock_path ]; then
    mkdir -p $install_lock_path
    echo "Init: Create Path: " $install_lock_path
fi

# 执行额外的配置文件
bash /app/docker/scripts/config.sh

# 设置环境变量默认值
if [ -z $CELERY_BEAT_LOG_LEVEL ]; then
    CELERY_BEAT_LOG_LEVEL=DEBUG
fi
if [ -z $CELERY_BEAT_LOG_FILE ]; then
    CELERY_BEAT_LOG_FILE=/app/runtime/log/celery/celeryd.log
fi
if [ -z $CELERY_WORKER_LOG_LEVEL ]; then
    CELERY_WORKER_LOG_LEVEL=DEBUG
fi
if [ -z $CELERY_WORKER_LOG_FILE ]; then
    CELERY_WORKER_LOG_FILE=/app/runtime/log/celery/%n%I.log
fi

# 对环境变量指定的路径进行创建
celery_beat_log_path=`dirname $CELERY_BEAT_LOG_FILE`
if [ ! -d $celery_beat_log_path ]; then
    mkdir -p $celery_beat_log_path
    echo "Init: Create Path: " $celery_beat_log_path
fi
celery_worker_log_path=`dirname $CELERY_WORKER_LOG_FILE`
if [ ! -d $celery_worker_log_path ]; then
    mkdir -p $celery_worker_log_path
    echo "Init: Create Path: " $celery_worker_log_path
fi

# 启动celery beat服务
echo "Exec: celery beat"
celery -A server beat -l $CELERY_BEAT_LOG_LEVEL --logfile=$CELERY_BEAT_LOG_FILE --pidfile= --detach

# 启动celery worker服务
echo "Exec: celery worker [default]"
celery -A server worker -Q default --hostname=default@%h -c $CELERY_WORKER_CONCURRENCY -l $CELERY_WORKER_LOG_LEVEL --logfile=$CELERY_WORKER_LOG_FILE --pidfile= --detach

echo "Exec: celery worker [email]"
celery -A server worker -Q email --hostname=email@%h -c $CELERY_WORKER_CONCURRENCY_EMAIL -l $CELERY_WORKER_LOG_LEVEL --logfile=$CELERY_WORKER_LOG_FILE --pidfile= --detach

echo "Exec: celery worker [crawl]"
celery -A server worker -Q crawl --hostname=crawl@%h -c $CELERY_WORKER_CONCURRENCY_CRAWL -l $CELERY_WORKER_LOG_LEVEL --logfile=$CELERY_WORKER_LOG_FILE --pidfile= --detach

# 完成全部安装初始化工作后创建安装锁文件
if [ ! -f "$INSTALL_LOCK_FILE" ]; then
    touch "$INSTALL_LOCK_FILE"
fi

if [ "$PRODUCTION" = "True" ]; then
    echo "> Production Mode"
    # 启动nginx
    echo "Exec: nginx"
    service nginx start

    # 启动gunicorn
    echo "Exec: gunicorn"
    exec "$@"
else
    echo "> Development Mode"
    echo "Exec: command"
    exec "$@"
fi
