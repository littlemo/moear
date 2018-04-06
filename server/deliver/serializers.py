import logging

from rest_framework import serializers
from deliver.models import DeliverLog
from spiders.models import Spider


log = logging.getLogger(__name__)


class DeliverLogSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        '''将输出的实例转成dict形式'''
        data = super().to_representation(instance)
        try:
            spider_pk = data.pop('spider')
            spider_obj = Spider.objects.get(pk=spider_pk)
            data['spider_display_name'] = spider_obj.display_name
            data['status_display'] = instance.get_status_display()
        except Exception:
            data = {}

        return data

    class Meta:
        model = DeliverLog
        exclude = ('id', 'users')
