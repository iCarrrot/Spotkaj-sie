"""
    Define urls
"""
from django.conf.urls import url
from django.contrib.auth.views import(
    LoginView,
    LogoutView,
)
from . import views


app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    url(r'^login/$', LoginView.as_view(template_name='polls/login.html'), name='login'),
    url(r'^logout/$', LogoutView.as_view(next_page='polls:index'), name='logout'),
    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^event/$', views.event, name='event'),
    url(r'^event(?P<event_id>[0-9]+)/$', views.new_event, name='new_event'),
    url(r'^plans/$', views.plans, name='plans'),
    url(r'^delete_events/$', views.delete_events, name='delete_events'),
    url(r'^delete_plans/$', views.delete_plans, name='delete_plans'),
]
