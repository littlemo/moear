from django.conf import settings
from django.urls import path, include

from rest_framework import routers

from restapi.views import SpiderAPIView


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]

spiders_urls = [
    path('spiders/', SpiderAPIView.as_view(), name='spiders'),
]

urlpatterns += spiders_urls
