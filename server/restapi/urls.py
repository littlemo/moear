from django.urls import path, include

from rest_framework import routers

from restapi.views import \
    SpiderEnabledSwitchAPIView, \
    SendInviteAPIView


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
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

urlpatterns += spiders_urls
urlpatterns += invite_urls
