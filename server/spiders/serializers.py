import logging

from rest_framework import serializers
from .models import *
from core.serializers import MetaListSerializer


log = logging.getLogger(__name__)


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    动态字段数据模型序列化器

    通过 ``exclude`` 字段从目标输出 ``fields`` 中排除指定的 field ，从而控制最终输出
    """

    def __init__(self, *args, **kwargs):
        # 不将 ``exclude`` 字段传到父类中
        fields = kwargs.pop('exclude', None)

        # 正常调用父类初始化方法
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # 去除所有列在 ``exclude`` 中的字段
            exclude = set(fields)
            for field_name in exclude:
                self.fields.pop(field_name, None)


class SpiderSerializer(DynamicFieldsModelSerializer):
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
        exclude = ('id',)
        extra_kwargs = {
            'name': {
                'validators': [],
            },
            'display_name': {
                'validators': [],
            },
        }


class SpiderMetaSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        '''若存在指定 Spider 的 name 字段数据，则执行更新操作，否则执行创建'''
        try:
            spidermeta = SpiderMeta.objects.get(
                spider=validated_data.get('spider', ''),
                name=validated_data.get('name', ''))
            return super().update(spidermeta, validated_data)
        except SpiderMeta.DoesNotExist:
            return super().create(validated_data)

    class Meta:
        model = SpiderMeta
        list_serializer_class = MetaListSerializer
        exclude = ('id',)
        extra_kwargs = {
            'spider': {
                'required': False,
            },
        }
