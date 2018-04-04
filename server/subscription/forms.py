from django import forms
from django.utils.translation import ugettext_lazy as _

from core.models import UserMeta


class DeliverSettingsForm(forms.Form):
    """
    投递设置表单
    """
    device_email = forms.EmailField(
        label=_('Kindle收件地址'),
        required=True,
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': _('E-mail address')}))

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
