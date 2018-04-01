from django.urls import path

from . import views

urlpatterns = [
    path('<path:path>/', views.page, name='page'),
    path('', views.page, name='index'),
]
