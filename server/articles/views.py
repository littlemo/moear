import logging
import os

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.html import format_html

from spider.spider.settings import PAGE_STORE, IMAGES_STORE
from .models import Article

logger = logging.getLogger(__name__)


def article_view(request, url_local):
    """
    文章页view请求处理方法，包含页面本体和其中的img请求处理逻辑
    :param request: 请求对象
    :param url_local: 请求url字串，格式为：<spider.name>/<pub_datetime>/[xxxx.html|img/xxxx.jpg]
    :return: 响应对象
    """
    logger.info('文章view请求url：{}'.format(url_local))

    # 处理文章页中的图片请求
    if 'img' in url_local:
        content_path = os.path.join(IMAGES_STORE, url_local)
        return FileResponse(open(content_path, 'rb'))

    # 处理文章页中的页面本体
    article = get_object_or_404(Article, url_local__contains=url_local)
    cover_image = '/'.join(article.cover_image_local.split('/')[-2:]) if any([article.cover_image_local]) else ''

    content_path = os.path.join(PAGE_STORE, article.url_local)
    logger.debug('文章本地路径：{}'.format(content_path))
    with open(content_path, 'r') as f:
        content = f.read()
    return render(request, 'articles/article.html',
                  {'article': article, 'cover_image': cover_image, 'content': content})
