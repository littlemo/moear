import logging
import copy

from rest_framework import serializers
from .models import *
from spiders.models import Spider


log = logging.getLogger(__name__)


class PostSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        """对传入的data进行修饰处理"""
        d = copy.deepcopy(data)
        spider_name = d.get('spider', None)
        try:
            d['spider'] = Spider.objects.get(name=spider_name).pk
        except Spider.DoesNotExist:
            d['spider'] = None
        ret = super().to_internal_value(d)
        return ret

    def create(self, validated_data):
        """若存在指定origin_url字段值的条目，则执行更新操作，否则执行创建"""
        try:
            post = Post.objects.get(
                origin_url=validated_data.get('origin_url', ''))
            return super().update(post, validated_data)
        except Post.DoesNotExist:
            return super().create(validated_data)

    class Meta:
        model = Post
        exclude = ('id', 'modified',)
        extra_kwargs = {
            'origin_url': {
                'validators': [],
            },
        }


class PostMetaListSerializer(serializers.ListSerializer):
    def to_internal_value(self, data):
        '''将传入的dict数据转换为符合数据模型的list形式'''
        data_dict = copy.deepcopy(data)
        data_list = []

        for (k, v) in data_dict.items():
            data_list.append({
                'name': k,
                'value': str(v),
            })

        return super().to_internal_value(data_list)

    def to_representation(self, instance):
        '''将输出的实例转成dict形式'''
        data_list = super().to_representation(instance)

        data_dict = {}
        for d in data_list:
            data_dict[d.get('name')] = d.get('value')

        return data_dict

    @property
    def data(self):
        return self.to_representation(self.instance)


class PostMetaSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        """若存在指定post的指定name字段数据，则执行更新操作，否则执行创建"""
        try:
            postmeta = PostMeta.objects.get(
                post=validated_data.get('post', ''),
                name=validated_data.get('name', ''))
            return super().update(postmeta, validated_data)
        except PostMeta.DoesNotExist:
            return super().create(validated_data)

    class Meta:
        model = PostMeta
        list_serializer_class = PostMetaListSerializer
        exclude = ('id',)
        extra_kwargs = {
            'post': {
                'required': False,
            },
        }
