from django.conf.urls import url

from . import views

app_name = 'articles'
urlpatterns = [
    # ex: /articles/zhihu_daily/2016-07-09/63d3f1ca7bedc9ff6a01c9acc3197a71ce3221b1.html
    url(r'^(?P<url_local>.+)$', views.article_view, name='article'),
]
