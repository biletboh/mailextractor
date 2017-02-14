from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# import google api credentials and flow fields
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.contrib.django_util.models import CredentialsField



# custom UserProfile model
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True,
            primary_key=True, on_delete=models.CASCADE,
            related_name='user_profile')
    gender = models.CharField(max_length=20, null=True, blank=True)
    image_url = models.CharField(max_length=512, null=True, blank=True) 
    
    def __unicode__(self):
        return u'%s profile' % self.user.username

# create Credentials 
class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()

# Restful email storage
class Emails(models.Model):
    email_id = models.CharField(primary_key=True, max_length=20)
    date = models.DateTimeField(auto_now=False,) 
    addresser = models.CharField(max_length=512, blank=True)
    addressee = models.CharField(max_length=2048, blank=True) 
    subject = models.CharField(max_length=1024, blank=True)
    body = models.TextField(blank=True)

    class Meta:
        ordering = ('-date',)
