import logging
import copy

from rest_framework import serializers
from .models import *


log = logging.getLogger(__name__)


class SpiderSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        '''若存在指定 name 字段值的条目，则执行更新操作，否则执行创建'''
        try:
            spider = Spider.objects.get(
                name=validated_data.get('name', ''))
            return super().update(spider, validated_data)
        except Spider.DoesNotExist:
            return super().create(validated_data)

    class Meta:
        model = Spider
        exclude = ('id', 'enabled')
        extra_kwargs = {
            'name': {
                'validators': [],
            },
        }
