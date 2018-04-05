from django.urls import path, include

from rest_framework import routers

from restapi.views import SpiderEnabledSwitchAPIView


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]

spiders_urls = [
    path(
        'spiders/switch/',
        SpiderEnabledSwitchAPIView.as_view(), name='spiders'),
]

urlpatterns += spiders_urls
