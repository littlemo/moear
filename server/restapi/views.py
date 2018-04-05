import logging

from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from invitations.models import Invitation

from spiders.models import Spider
from spiders.serializers import SpiderSerializer

log = logging.getLogger(__name__)


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
