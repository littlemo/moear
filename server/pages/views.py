import os
import logging

from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.utils._os import safe_join
from django.utils.translation import gettext_lazy as _

log = logging.getLogger(__name__)


def check_page_or_404(name):
    """
    检查待访问页面是否存在，不存在则抛出404错误
    """
    try:
        file_path = safe_join(settings.SITE_PAGES_DIR, name)
    except ValueError:
        raise Http404(_('页面未找到'))
    else:
        if not os.path.exists(file_path):
            raise Http404(_('页面未找到'))


def page(request, path='index'):
    """
    如果找到，则渲染请求的页面
    """
    log.debug('path => {}'.format(path))
    if path.startswith('_'):
        log.info('访问了Web组件隐藏路径！[{}]'.format(path))
        raise Http404(_('页面未找到'))
    file_name = '{}.html'.format(path)
    check_page_or_404(file_name)
    context = {
    }
    return render(request, 'pages/{}.html'.format(path), context)
