from django import forms
from django.utils.translation import ugettext_lazy as _

from core.models import UserMeta
from spiders.models import Spider


class DeliverSettingsForm(forms.Form):
    """
    投递设置表单
    """
    device_email = forms.EmailField(
        label=_('Kindle收件地址'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'email',
                'placeholder': _('Kindle收件地址')}))

    def save(self, request, **kwargs):
        device_email = self.cleaned_data['device_email']
        um, created = UserMeta.objects.get_or_create(
            user=request.user,
            name=UserMeta.MOEAR_DEVICE_ADDR,
            defaults={
                'value': device_email,
            })
        if not created:
            um.value = device_email
            um.save()
        return um

    def as_div(self):
        return self._html_output(
            normal_row='<div class="form-group my-1 form-inline">'
                       '%(field)s%(errors)s%(help_text)s</div>',
            error_row='<span class="text-danger mx-2">%s</span>',
            row_ender='</div>',
            help_text_html='<br /><span class="helptext">%s</span>',
            errors_on_separate_row=False)


class PostSubscribeForm(forms.Form):
    '''
    文章订阅表单
    '''
    feeds_choices = [('', _('取消订阅'))] + [
        (spider.name, spider.display_name)
        for spider in Spider.objects.filter(enabled=True)]
    feeds = forms.MultipleChoiceField(
        label=_('源'),
        help_text=_('按住 ”Control“，或者Mac上的 “Command”，可以选择多个。'),
        choices=feeds_choices,
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control',
            }))

    def save(self, request, **kwargs):
        feeds = ','.join(self.cleaned_data['feeds'])
        um, created = UserMeta.objects.get_or_create(
            user=request.user,
            name=UserMeta.MOEAR_SPIDER_FEEDS,
            defaults={
                'value': feeds,
            })
        if not created:
            um.value = feeds
            um.save()
        return um

    def as_div(self):
        return self._html_output(
            normal_row='<div class="form-group my-1">'
                       '%(label)s %(field)s%(errors)s%(help_text)s</div>',
            error_row='<span class="text-danger mx-2">%s</span>',
            row_ender='</div>',
            help_text_html='<small class="text-muted">%s</small>',
            errors_on_separate_row=False)
