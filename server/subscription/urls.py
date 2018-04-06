from django.urls import path

from subscription.views import MySubscribeView

urlpatterns = [
    path(
        'my_subscribe/', MySubscribeView.as_view(),
        name='subscription_my_subscribe'),
]
