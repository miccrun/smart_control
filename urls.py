
from django.conf.urls import patterns, url

import apps.control.views as ControlViews
import apps.auth.views as AuthViews

urlpatterns = patterns('',
    url(r'^$', ControlViews.DashboardView.as_view(), name='dashboard'),
    url(r'^operate$', ControlViews.OperateView.as_view(), name='operate'),
    url(r'^event/(?P<event_id>\d+)$', ControlViews.EventView.as_view(), name='event'),

    url(r'^login$', AuthViews.LoginView.as_view(), name='login'),
    url(r'^logout$', AuthViews.LogoutView.as_view(), name='logout'),
    url(r'^register$', AuthViews.RegisterView.as_view(), name='register'),
)
