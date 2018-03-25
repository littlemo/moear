import stevedore

from django.core.management.base import BaseCommand, CommandError

from spiders.models import Spider, SpiderMeta


class Command(BaseCommand):
    help = '遍历已安装的 Python 包，并注册其中的 Spider 插件'

    def handle(self, *args, **options):
        mgr = stevedore.ExtensionManager(
            namespace='moear.spider',
            invoke_on_load=True)

        def register_spdier(ext):
            self.stdout.write(self.style.SUCCESS(
                '注册: [{name}]{data}'.format(
                    name=ext.name,
                    data=ext.obj.register())))

        results = mgr.map(register_spdier)
