
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import (
    FormView,
    View,
)

from apps.auth.forms import (
    LoginForm,
    RegisterForm,
)


class LoginRequiredMixin(object):

    @method_decorator(login_required(redirect_field_name='redirect'))
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class AuthView(FormView):

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super(AuthView, self).form_valid(form)


class LoginView(AuthView):
    template_name = 'auth/login.html'
    form_class = LoginForm

    def get_success_url(self):
        return self.request.POST.get('redirect', '/')

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['redirect'] = self.request.GET.get('redirect', '/')
        return context


class RegisterView(AuthView):
    template_name = 'auth/register.html'
    form_class = RegisterForm
    success_url = '/'


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
