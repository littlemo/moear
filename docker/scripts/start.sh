#!/usr/bin/env bash

# 执行额外的配置文件
bash /app/run/config.sh

# 设置环境变量默认值
if [ -z $CELERY_BEAT_LOG_LEVEL ];then
    CELERY_BEAT_LOG_LEVEL=DEBUG
fi
if [ -z $CELERY_BEAT_LOG_FILE ];then
    CELERY_BEAT_LOG_FILE=/app/runtime/log/celery/celeryd.log
fi
if [ -z $CELERY_WORKER_LOG_LEVEL ];then
    CELERY_WORKER_LOG_LEVEL=DEBUG
fi
if [ -z $CELERY_WORKER_LOG_FILE ];then
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
echo "Exec: celery worker"
celery -A server worker -l $CELERY_WORKER_LOG_LEVEL --logfile=$CELERY_WORKER_LOG_FILE --pidfile= --detach

if [ "$PRODUCTION" = "True" ];then
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
