from django.db import models
from django.utils.translation import ugettext_lazy as _


class Option(models.Model):
    """
    站点配置

    网站的设置和选项，用于设置站点信息、插件相关等额外配置
    """
    YES = 'yes'
    NO = 'no'
    AUTOLOAD_CHOICES = (
        (YES, _('是')),
        (NO, _('否')),
    )

    # 系统配置项属性名
    OPEN_FOR_SIGNUP = 'open_for_signup'  #: 开放注册

    id = models.BigAutoField(
        primary_key=True)
    name = models.CharField(
        verbose_name=_('键名'),
        db_index=True,
        unique=True,
        max_length=255)
    value = models.TextField(
        verbose_name=_('键值'))
    autoload = models.CharField(
        verbose_name=_('自动载入'),
        blank=True,
        default=YES,
        choices=AUTOLOAD_CHOICES,
        max_length=20)

    @property
    def open_for_signup(self):
        return Option.get_bool_value(Option.OPEN_FOR_SIGNUP, False)

    @open_for_signup.setter
    def open_for_signup(self, value):
        Option.set_bool_value(Option.OPEN_FOR_SIGNUP, value)

    @staticmethod
    def _get_value_by_name(name, default=''):
        opt, _ = Option.objects.get_or_create(
            name=name,
            defaults={
                'value': default
            })
        return opt.value

    @staticmethod
    def get_bool_value(name, default=False):
        if not isinstance(default, str):
            default = 'true' if default else 'false'
        value = Option._get_value_by_name(name, default)
        if isinstance(value, bool):
            return value
        return value.lower() == 'true'

    @staticmethod
    def get_int_value(name, default=0):
        if not isinstance(default, str):
            default = str(default)
        value = Option._get_value_by_name(name, default)
        if isinstance(value, int):
            return value
        return int(value)

    @staticmethod
    def get_str_value(name, default=''):
        if not isinstance(default, str):
            default = str(default)
        value = Option._get_value_by_name(name, default)
        if isinstance(value, str):
            return value
        return str(value)

    @staticmethod
    def _set_value_by_name(name, value):
        opt, created = Option.objects.get_or_create(
            name=name,
            defaults={
                'value': value,
            })
        if not created:
            opt.value = value
            opt.save()

    @staticmethod
    def set_bool_value(name, value):
        if not isinstance(value, bool):
            raise TypeError('value 类型错误：{}'.format(type(value)))
        value = 'true' if value else 'false'
        Option._set_value_by_name(name, value)

    @staticmethod
    def set_int_value(name, value):
        if not isinstance(value, int):
            raise TypeError('value 类型错误：{}'.format(type(value)))
        value = str(value)
        Option.set_value_by_name(name, value)

    @staticmethod
    def set_str_value(name, value):
        if not isinstance(value, str):
            raise TypeError('value 类型错误：{}'.format(type(value)))
        Option.set_value_by_name(name, value)

    def __str__(self):
        return '[{id}]{name} => {value}'.format(
            id=self.id,
            name=self.name,
            value=self.value)

    class Meta:
        verbose_name = _('站点配置')
        verbose_name_plural = verbose_name


class UserMeta(models.Model):
    """
    用户元数据模型

    用于存储指定用户的元数据信息，便于对该用户进行参数定制修改，可与插件/爬虫配合使用
    """
    # 用户元数据项属性名
    MOEAR_DEVICE_ADDR = 'moear.device.addr'  #: 设备收件地址
    MOEAR_SPIDER_FEEDS = 'moear.spider.feeds'  #: 用户订阅列表

    id = models.BigAutoField(
        primary_key=True)
    user = models.ForeignKey(
        'auth.User',
        verbose_name=_('用户信息'),
        db_index=True,
        on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name=_('键名'),
        db_index=True,
        max_length=255)
    value = models.TextField(
        verbose_name=_('键值'),
        blank=True,
        default='')

    def __str__(self):
        output = '[{id}]{name} => {value}'.format(
            id=self.id,
            name=self.name,
            value=self.value)
        return output

    class Meta:
        verbose_name = _('用户元数据')
        verbose_name_plural = verbose_name
