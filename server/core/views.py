from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, TemplateView

from invitations.utils import get_invite_form
from deliver.models import DeliverLog

InviteForm = get_invite_form()


class SendInvite(FormView):
    template_name = 'invitations/forms/_invite.html'
    form_class = InviteForm

    # 当前邀请功能仅对"superuser"开放
    @method_decorator(user_passes_test(
        lambda u: u.is_superuser, login_url='/'))
    def dispatch(self, request, *args, **kwargs):
        return super(SendInvite, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        try:
            invite = form.save(email)
            invite.inviter = self.request.user
            invite.save()
            invite.send_invitation(self.request)
        except Exception:
            return self.form_invalid(form)
        return self.render_to_response(
            self.get_context_data(
                success_message=_('%(email)s has been invited') % {
                    "email": email}))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class MySubscribeView(TemplateView):
    """
    我的订阅视图

    主要包含三块内容：文章订阅(Form)，投递设置(Form)，投递日志
    """
    template_name = 'subscription/my-subscribe.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['deliver_log'] = DeliverLog.objects.filter(
            users=request.user).order_by('-date')[:10]
        return self.render_to_response(context)
