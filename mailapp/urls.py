from django.conf.urls import url
from django.contrib.auth import views as auth_views
from social_django.urls import urlpatterns 

from . import views

urlpatterns = [
    url(r'^$', auth_views.login, {'template_name':
        'mailapp/social-login.html'} , name = 'social-login'),
    url(r'^mails/$', views.Mails.as_view(), name='profile'),
    url(r'^logout/$', views.logout, name='logout'),
]
