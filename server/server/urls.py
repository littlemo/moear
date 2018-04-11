"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = []

if settings.DJANGO_ADMIN_URL:
    urlpatterns.append(
        path(
            '{}/doc/'.format(settings.DJANGO_ADMIN_URL),
            include('django.contrib.admindocs.urls')))
    urlpatterns.append(
        path('{}/'.format(settings.DJANGO_ADMIN_URL), admin.site.urls))

urlpatterns += [
    path('subscription/', include('subscription.urls')),
    path('accounts/', include('allauth.urls')),
    path('invitations/', include('invitations.urls', namespace='invitations')),
    path('api/', include('restapi.urls')),
    path('', include('pages.urls')),
]
