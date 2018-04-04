from django.urls import path

from . import views

urlpatterns = [
    path(
        'post_subscribe/', views.PostSubscribeView.as_view(),
        name='subscription_post_subscribe'),
    path(
        'deliver_settings/', views.DeliverSettingsView.as_view(),
        name='subscription_deliver_settings'),
    path(
        'deliver_log/', views.DeliverLogView.as_view(),
        name='subscription_deliver_log'),
]
