
from django.views.generic import (
    TemplateView,
)

from apps.auth.views import LoginRequiredMixin

from apps.control.models import (
    Device,
)


#class DashboardView(LoginRequiredMixin, ListView):
class DashboardView(TemplateView):
    template_name = 'control/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['data'] = 'hello world'
        return context
