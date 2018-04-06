import logging

from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from invitations.models import Invitation

from core.models import UserMeta
from spiders.models import Spider
from spiders.serializers import SpiderSerializer
from deliver.models import DeliverLog
from deliver.serializers import DeliverLogSerializer

log = logging.getLogger(__name__)


class SpiderSubscribeSwitchAPIView(APIView):
    '''
    爬虫订阅切换接口
    ----------------

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


class DeliverLogAPIView(APIView):
    '''
    投递日志获取接口
    ----------------

    列出当前用户的投递日志，目前仅显示最近10条
    '''
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        deliver_log = DeliverLog.objects.filter(
            users=request.user).order_by('-date')[:10]
        deliver_log_serializer = DeliverLogSerializer(deliver_log, many=True)
        return Response(deliver_log_serializer.data, status=status.HTTP_200_OK)


class SpiderEnabledSwitchAPIView(APIView):
    '''
    爬虫开关切换接口
    ----------------

    列出所有 Spider ，或者更新某一个 Spider 的开关状态
    '''
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        spiders_obj = Spider.objects.all()
        spiders_list = SpiderSerializer(spiders_obj, many=True)
        log.debug(_('爬虫列表: {}'.format(spiders_list.data)))
        return Response(spiders_list.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        '''
        用例::

            {
                "name": "zhihu_daily",
                "enabled": false
            }
        '''
        spider_name = request.data.get('name', None)
        spider_enabled = request.data.get('enabled', True)
        if not spider_name:
            return Response(
                _('name 字段为空'), status=status.HTTP_400_BAD_REQUEST)
        try:
            spider = Spider.objects.get(name=spider_name)
        except Spider.DoesNotExist:
            return Response(_('name({name}) 指定的 Spider 不存在').format(
                name=spider_name), status=status.HTTP_404_NOT_FOUND)
        spider.enabled = spider_enabled
        spider.save()
        serializer = SpiderSerializer(spider)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SendInviteAPIView(APIView):
    '''
    发送邀请接口
    ------------

    发送注册邀请
    '''
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, format=None):
        '''
        用例::

            {
                "email": "xx@yyy.zzz"
            }
        '''
        email = request.data.get('email', None)
        log.info('email: {}'.format(email))
        if not email:
            return Response(
                _('email 字段为空'), status=status.HTTP_400_BAD_REQUEST)
        f = forms.EmailField()
        try:
            email = f.clean(email)
        except ValidationError as e:
            return Response(
                _('Email 值错误：{}'.format(', '.join(e))),
                status=status.HTTP_400_BAD_REQUEST)
        try:
            invite = Invitation.create(email, inviter=self.request.user)
            invite.save()
            invite.send_invitation(self.request)
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(
            _('已发送注册邀请邮件到【{email}】').format(email=email))
