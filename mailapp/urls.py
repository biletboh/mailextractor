from django.conf.urls import url
from django.contrib.auth import views as auth_views
from social_django.urls import urlpatterns 

from . import views

urlpatterns = [
    url(r'^$', auth_views.login, kwargs={'redirect_authenticated_user': True, 
        'template_name':'mailapp/social-login.html',}, 
        name = 'social-login'),
    url(r'^profile/$', views.Mails.as_view(), name='profile'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/mails/$', views.index, name='gmail'),
    url(r'^oauth2callback/gmail', views.auth_return, name="oauth2callback-gmail"),
]
