import json
import stevedore

from django.core.management.base import BaseCommand, CommandError
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from spiders.models import SpiderMeta
from spiders.serializers import SpiderSerializer, SpiderMetaSerializer


class Command(BaseCommand):
    help = '遍历已安装的 Python 包，并注册其中的 Spider 插件'

    def handle(self, *args, **options):
        mgr = stevedore.ExtensionManager(
            namespace='moear.spider',
            invoke_on_load=True)

        def register_spdier(ext):
            data = ext.obj.register()

            # 持久化Spider数据
            spider_serializer = SpiderSerializer(
                data=data, exclude=['enabled'])
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

            # 创建计划任务
            spider = spider_serializer.instance
            crawl_schedule = SpiderMeta.objects.get(
                spider=spider,
                name='crawl_schedule').value
            crawl_schedule_list = crawl_schedule.split()
            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute=crawl_schedule_list[0],
                hour=crawl_schedule_list[1],
                day_of_week=crawl_schedule_list[2],
                day_of_month=crawl_schedule_list[3],
                month_of_year=crawl_schedule_list[4])
            task_name = 'core.tasks.periodic_chain_crawl_package_deliver'
            try:
                periodic_task = PeriodicTask.objects.get(
                    name='Crawl Spider [{}]'.format(spider.name))
                periodic_task.crontab = schedule
                periodic_task.task = task_name
                periodic_task.save()
            except PeriodicTask.DoesNotExist:
                periodic_task = PeriodicTask.objects.create(
                    crontab=schedule,
                    name='Crawl Spider [{}]'.format(spider.name),
                    task=task_name,
                    args=json.dumps([spider.name]),
                )
            spider.save()  # 根据Spider使能配置，更新计划任务的使能状态

            self.stdout.write(self.style.SUCCESS(
                '[{name}] 注册成功！'.format(
                    name=ext.name)))

        mgr.map(register_spdier)
