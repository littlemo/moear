import stevedore

from django.core.management.base import BaseCommand, CommandError

from spiders.models import *
from spiders.serializers import *


class Command(BaseCommand):
    help = '遍历已安装的 Python 包，并注册其中的 Spider 插件'

    def handle(self, *args, **options):
        mgr = stevedore.ExtensionManager(
            namespace='moear.spider',
            invoke_on_load=True)

        def register_spdier(ext):
            data = ext.obj.register()

            # 持久化Spider数据
            spider_serializer = SpiderSerializer(data=data)
            if not spider_serializer.is_valid():
                self.stderr.write(self.style.ERROR(spider_serializer.errors))
                raise CommandError(spider_serializer.errors)
            spider_serializer.save()

            # 持久化SpiderMeta数据
            spidermeta_serializer = SpiderMetaSerializer(
                data=data.get('meta', {}), many=True)
            if not spidermeta_serializer.is_valid():
                self.stderr.write(self.style.ERROR(
                    spidermeta_serializer.errors))
                raise CommandError(spidermeta_serializer.errors)
            spidermeta_serializer.save(spider=spider_serializer.instance)

            self.stdout.write(self.style.SUCCESS(
                '[{name}] 注册成功！'.format(
                    name=ext.name)))

        mgr.map(register_spdier)
