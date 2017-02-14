# basic imports 
import os
import httplib2
import logging
import base64
from datetime import datetime
from dateutil import parser

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User 
from models import Emails
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from cayugatestapp import settings

# auth imports
from django.contrib.auth import logout as auth_logout

# google api
from googleapiclient.discovery import build
from models import CredentialsModel
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage

# rest framework
from rest_framework import viewsets
from serializers import EmailsSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from serializers import EmailsSerializer 

# import client secrets 
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 
'client_secrets.json')

# create FLOW object for gmail api extraction 
FLOW = flow_from_clientsecrets(
        CLIENT_SECRETS,
        scope='https://www.googleapis.com/auth/gmail.readonly',
        redirect_uri='http://localhost:8000/oauth2callback/gmail/')

# process gmail api, step 1
@login_required
def index(request):
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()

    # validate creadentials
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)

        # access gmail api
        service = build("gmail", "v1", http=http)
        messageslist = service.users().messages().list(userId='me').execute()

        # extract 100 mails
        messageslist = messageslist.get('messages', [])[0:100]

        # access to full and raw Gmail api
        full_messageslist = []

        # raw_messageslist = [] ### uncomment to retrieve raw mail data

        for message in messageslist:
            full_msg = service.users().messages().get(userId='me', id =
                    message['id'], format='full').execute()
            #raw_msg = service.users().messages().get(userId='me', id =
            #        message['id'], format='raw').execute() ### uncomment to retrieve raw mail data

            
            full_messageslist.append(full_msg)

            # extract, save, and update data for custom REST api 
            full = full_msg['id']
            for e in full_msg['payload']['headers']: 
                if e['name'] == 'From':
                    addresser = e['value']
                if e['name'] == 'To':
                    addressee = e['value'] 
                if e['name'] == 'Date':
                    date = e['value']
                if e['name'] == 'Subject':
                    subject = e['value']

            # encode body of the text to UTF8
            try:
                body = base64.urlsafe_b64decode(full_msg['payload']['parts'][0]['body']['data'].encode('UTF8'))
            except:
                body = ''

            # format date  
            formated_date = parser.parse(date)
            email, created = Emails.objects.get_or_create(email_id =
                    full_msg['id'], date = formated_date)            
            email.addresser = addresser
            email.addressee = addressee
            email.subject = subject
            email.body = body 
            email.save()

        # log data and return it
        logging.info(full_messageslist)
        return render(request, 'mailapp/apiredirect.html', 
               # {'messageslist': full_messageslist,}
                ) 

# process gmail api, step 2
@login_required
def auth_return(request):
    # validate token 
    if not xsrfutil.validate_token(settings.SECRET_KEY,
        request.GET['state'], 
        request.user):
        return  HttpResponseBadRequest()

    # get creadentials and store them 
    credential = FLOW.step2_exchange(request.GET)
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/profile/mails") 

# render rest emails
class EmailsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Emails.objects.all()    
    serializer_class = EmailsSerializer

# handle pofile pages
class Mails(LoginRequiredMixin, ListView):
    template_name = 'mailapp/mails.html'
    model = User
    def get_context_data(self, **kwargs):
        context = super(Mails, self).get_context_data(**kwargs)
        context['title'] = "Mails content API"
        return context

# logout from the app
@login_required
def logout(request):
    auth_logout(request)
    return redirect('/')
