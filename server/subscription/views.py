from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView
from django.contrib.auth.decorators import login_required

from core.models import UserMeta
from deliver.models import DeliverLog
from subscription.forms import DeliverSettingsForm, PostSubscribeForm


class DeliverLogView(TemplateView):
    '''
    投递日志视图
    '''
    template_name = 'subscription/deliver_log.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['deliver_log'] = DeliverLog.objects.filter(
            users=request.user).order_by('-date')[:10]
        return self.render_to_response(context)


class DeliverSettingsView(FormView):
    """
    投递设置视图
    """
    template_name = 'subscription/deliver_settings.html'
    form_class = DeliverSettingsForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DeliverSettingsView, self).dispatch(
            request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            um = UserMeta.objects.get(
                user=request.user,
                name=UserMeta.MOEAR_DEVICE_ADDR)
            settings_data = {
                'device_email': um.value,
            }
        except UserMeta.DoesNotExist:
            settings_data = None
        form = self.form_class(
            data=settings_data)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        device_email = form.cleaned_data['device_email']
        try:
            form.save(self.request)
        except Exception:
            return self.form_invalid(form)
        msg = _('投递地址【{device_email}】设置成功！').format(
            device_email=device_email)
        messages.add_message(self.request, messages.SUCCESS, msg)
        return self.render_to_response(self.get_context_data())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class PostSubscribeView(FormView):
    """
    文章订阅视图
    """
    template_name = 'subscription/post_subscribe.html'
    form_class = PostSubscribeForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PostSubscribeView, self).dispatch(
            request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            um = UserMeta.objects.get(
                user=request.user,
                name=UserMeta.MOEAR_SPIDER_FEEDS)
            settings_data = {
                'feeds': um.value.split(','),
            }
        except UserMeta.DoesNotExist:
            settings_data = None
        form = self.form_class(
            data=settings_data)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        try:
            form.save(self.request)
        except Exception:
            return self.form_invalid(form)
        msg = _('订阅设置成功！')
        messages.add_message(self.request, messages.SUCCESS, msg)
        return self.render_to_response(self.get_context_data())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
