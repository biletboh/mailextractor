from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from mailapp import views

# test django rest framework
router = routers.DefaultRouter()
router.register(r'emails', views.EmailsViewSet)

urlpatterns = [
    # app urls 
    url(r'^', include('mailapp.urls', namespace='mailapp')),

    # django social urls
    url('', include('social_django.urls', namespace='social')),

    # rest api urls
    url(r'^emails-api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
    namespace='rest_framework')),

    # admin urls
    url(r'^admin/', admin.site.urls),
]
