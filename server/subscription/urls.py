from django.urls import path

from . import views

urlpatterns = [
    path(
        'deliver_log/', views.DeliverLogView.as_view(),
        name='subscription_deliver_log'),
]
