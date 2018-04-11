import logging

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from invitations.models import Invitation

log = logging.getLogger(__name__)


class SendInviteAPIView(APIView):
    '''
    发送邀请接口

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
            _('已发送注册邀请邮件到【{email}】').format(email=email),
            status=status.HTTP_200_OK)
