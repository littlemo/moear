import logging

from rest_framework import serializers
from .models import *


log = logging.getLogger(__name__)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('id', 'modified',)


class PostMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMeta
        exclude = ('id',)
