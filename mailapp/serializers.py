from django.contrib.auth.models import User, Group 
from models import Emails
from rest_framework import serializers

class EmailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Emails 
        fields = ('url', 'email_id', 'date', 'addresser', 'addressee', 'subject', 'body')

