import logging

from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from spiders.models import Spider
from spiders.serializers import SpiderSerializer

log = logging.getLogger(__name__)


class SpiderAPIView(APIView):
    '''
    爬虫列表
    --------

    列出所有 Spider ，或者更新某一个 Spider 的开关状态
    '''
    def get(self, request, format=None):
        spiders_obj = Spider.objects.all()
        spiders_list = SpiderSerializer(spiders_obj, many=True)
        log.debug(_('爬虫列表: {}'.format(spiders_list.data)))
        return Response(spiders_list.data, status=status.HTTP_200_OK)
