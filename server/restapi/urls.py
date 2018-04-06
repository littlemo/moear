from django.urls import path, include

from rest_framework import routers

from spiders.views import \
    SpiderEnabledSwitchAPIView
from core.views import \
    SendInviteAPIView
from subscription.views import \
    SpiderSubscribeSwitchAPIView, \
    DeliverSettingsAPIView, \
    DeliverLogAPIView


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
]

subscribe_urls = [
    path(
        'subscribe/',
        SpiderSubscribeSwitchAPIView.as_view(), name='api_subscribe')
]

deliver_urls = [
    path(
        'deliver/settings/',
        DeliverSettingsAPIView.as_view(), name='api_deliver_settings'),
    path(
        'deliver/log/',
        DeliverLogAPIView.as_view(), name='api_deliver_log')
]

spiders_urls = [
    path(
        'spiders/switch/',
        SpiderEnabledSwitchAPIView.as_view(), name='api_spiders'),
]

invite_urls = [
    path(
        'invite/',
        SendInviteAPIView.as_view(), name='api_invite')
]

urlpatterns += subscribe_urls
urlpatterns += deliver_urls
urlpatterns += spiders_urls
urlpatterns += invite_urls
