# basic imports 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# auth imports
from django.contrib.auth import logout as auth_logout

# google api
from googleapiclient.discovery import build

# rest framework
from rest_framework import viewsets
from serializers import UserSerializer, GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

#View that handles Profile pages

class Mails(LoginRequiredMixin, ListView):
    template_name = 'mailapp/mails.html'
    model = User
    def get_context_data(self, **kwargs):
        context = super(Mails, self).get_context_data(**kwargs)
        context['title'] = "Mails content API"
        return context

#def mails(request):
#    context = {}
#    template = 'mailapp/mails.html'
#    return render(request, template, context)

def logout(request):
    auth_logout(request)
    return redirect('/')
