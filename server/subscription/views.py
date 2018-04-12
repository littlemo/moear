import logging
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from core.models import UserMeta
from deliver.models import DeliverLog
from spiders.models import Spider
from deliver.serializers import DeliverLogSerializer
from spiders.serializers import SpiderSerializer

log = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class MySubscribeView(TemplateView):
    template_name = 'subscription/my_subscribe.html'

    def get_context_data(self, **kwargs):
        kwargs['default_from_email'] = settings.DEFAULT_FROM_EMAIL
        return super().get_context_data(**kwargs)


class SpiderSubscribeSwitchAPIView(APIView):
    '''
    爬虫订阅切换接口

    列出所有 Spider ，或者更新某一个 Spider 的开关状态
    '''
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        spiders_obj = Spider.objects.filter(enabled=True)
        spiders_list = SpiderSerializer(
            spiders_obj, many=True, exclude=['enabled'])
        log.debug(_('爬虫订阅列表: {}'.format(spiders_list.data)))

        um, created = UserMeta.objects.get_or_create(
            user=request.user,
            name=UserMeta.MOEAR_SPIDER_FEEDS,
            defaults={
                'value': '',
            })
        subscribe_list = um.value and um.value.split(',')
        return Response(
            {
                'spiders_list': spiders_list.data,
                'subscribe_list': subscribe_list or [],
            }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        '''
        用例::

            {
                "name": "zhihu_daily",
                "subscribe": false
            }
        '''
        spider_name = request.data.get('name', None)
        spider_subscribe = request.data.get('subscribe', True)
        if not spider_name:
            return Response(
                _('name 字段为空'), status=status.HTTP_400_BAD_REQUEST)
        try:
            Spider.objects.get(name=spider_name)
        except Spider.DoesNotExist:
            return Response(_('指定的 Spider【{name}】 不存在').format(
                name=spider_name), status=status.HTTP_404_NOT_FOUND)

        feed = spider_name if spider_subscribe else ''
        um, created = UserMeta.objects.get_or_create(
            user=request.user,
            name=UserMeta.MOEAR_SPIDER_FEEDS,
            defaults={
                'value': feed,
            })
        if not created:
            feeds = set(um.value.split(','))
            log.info(feeds)
            if spider_subscribe:
                feeds.add(spider_name)
                log.info(feeds)
            if not spider_subscribe and spider_name in feeds:
                feeds.remove(spider_name)
                log.info(feeds)
            if '' in feeds:
                feeds.remove('')
            um.value = ','.join(feeds)
            log.info(um.value)
            um.save()
        return Response(feeds, status=status.HTTP_201_CREATED)


class DeliverSettingsAPIView(APIView):
    '''
    投递设置接口

    投递参数设置，更新当前用户的投递设置
    '''
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        um_device_addr, created = UserMeta.objects.get_or_create(
            user=request.user,
            name=UserMeta.MOEAR_DEVICE_ADDR,
            defaults={
                'value': '',
            })
        return Response(
            {
                'device_addr': um_device_addr.value,
            }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        '''
        用例::

            {
                "device_addr": "xx@yyy.zzz"
            }
        '''
        um_device_addr = request.data.get('device_addr', None)
        log.info('um_device_addr: {}'.format(um_device_addr))
        f = forms.EmailField(required=False)
        try:
            um_device_addr = f.clean(um_device_addr)
        except ValidationError as e:
            return Response({
                'device_addr': {
                    'rc': False,
                    'msg': _('Email 值错误：{}').format(', '.join(e))
                },
            }, status=status.HTTP_200_OK)
        try:
            um, created = UserMeta.objects.get_or_create(
                user=request.user,
                name=UserMeta.MOEAR_DEVICE_ADDR,
                defaults={
                    'value': um_device_addr,
                })
            if not created:
                um.value = um_device_addr
                um.save()
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            'device_addr': {
                'rc': True,
            }
        }, status=status.HTTP_200_OK)


class DeliverLogAPIView(APIView):
    '''
    投递日志获取接口

    列出当前用户的投递日志，目前仅显示最近10条
    '''
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        deliver_log = DeliverLog.objects.filter(
            users=request.user).order_by('-date')[:10]
        deliver_log_serializer = DeliverLogSerializer(deliver_log, many=True)
        return Response(deliver_log_serializer.data, status=status.HTTP_200_OK)
