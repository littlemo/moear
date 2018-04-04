from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView
from django.contrib.auth.decorators import login_required
from deliver.models import DeliverLog
from .forms import DeliverSettingsForm
from core.models import UserMeta


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
