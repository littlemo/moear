import logging

from rest_framework import serializers
from .models import *
from spiders.models import Spider


log = logging.getLogger(__name__)


class PostSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        """对传入的data进行修饰处理"""
        spider_name = data.get('spider', None)
        try:
            data['spider'] = Spider.objects.get(name=spider_name).pk
        except Spider.DoesNotExist:
            data['spider'] = None
        ret = super().to_internal_value(data)
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
        exclude = ('id',)
