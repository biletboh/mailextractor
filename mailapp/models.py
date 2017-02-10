from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

#from django.db.models.signals import post_save
#from django.dispatch import receiver
#from oauth2client.contrib.django_orm import CredentialsField, FlowField

#class FlowModel(models.Model):
#    id = models.ForeignKey(User, primary_key=True)
#    flow = FlowField()

# custom UserProfile model

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True,
            primary_key=True, on_delete=models.CASCADE,
            related_name='user_profile')
    gender = models.CharField(max_length=20, null=True, blank=True)
    image_url = models.CharField(max_length=512, null=True, blank=True) 
    
    def __unicode__(self):
        return u'%s profile' % self.user.username
