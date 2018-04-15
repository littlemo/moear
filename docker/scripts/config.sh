#!/bin/bash -x

if [ "$DEBUG" = "True" ]; then
# 在调试模式下，进行Python包的可编辑安装

# 以可编辑模式安装插件包以及项目包依赖
pip install --no-cache-dir -e /app/requirements/source/moear-api-common
pip install --no-cache-dir -e /app/requirements/source/moear-package-*
pip install --no-cache-dir -e /app/requirements/source/moear-spider-*
pip install --no-cache-dir -r /app/requirements/pip.txt

else
# 在非调试模式下，进行 wheel 包的更新安装

# 更新插件包安装
pip install --no-cache-dir /app/requirements/wheels/moear_api_common*.whl
pip install --no-cache-dir /app/requirements/wheels/moear_package_*.whl
pip install --no-cache-dir /app/requirements/wheels/moear_spider_*.whl

fi


# 初始化数据库表格
python manage.py makemigrations --settings=$SERVER_SETTINGS --noinput
python manage.py makemigrations --settings=$SERVER_SETTINGS --noinput posts spiders terms core deliver
python manage.py migrate --settings=$SERVER_SETTINGS --noinput


# 仅在安装时执行的命令
if [ ! -f "$INSTALL_LOCK_FILE" ]; then

# 创建超级管理员账户，若已存在则更新其密码
python manage.py create_superuser
# 填充站点数据
python manage.py loaddata --settings=$SERVER_SETTINGS Site.json
# 填充站点配置数据
python manage.py loaddata --settings=$SERVER_SETTINGS Option.json
# 生成version.py文件
python /app/hooks/update_version_file.py

fi


# 注册全部 Spider
python manage.py register_spiders --settings=$SERVER_SETTINGS


# 仅在生产模式下执行静态资源归集&翻译文件生成等操作
if [ "$PRODUCTION" = "True" ]; then

# 归集静态文件
python manage.py collectstatic --noinput

# 更新&编译翻译文件
python manage.py makemessages --settings=$SERVER_SETTINGS --all
python manage.py makemessages --settings=$SERVER_SETTINGS --domain djangojs --all --ignore echarts.js --ignore bootstrap.js --ignore jquery.js
python manage.py compilemessages --settings=$SERVER_SETTINGS

fi
