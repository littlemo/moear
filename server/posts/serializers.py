import logging

from rest_framework import serializers
from .models import *


log = logging.getLogger(__name__)


class PostSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = PostMeta
        exclude = ('id',)
