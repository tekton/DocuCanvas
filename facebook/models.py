import json, urllib

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin



class Facebook(models.Model):
    user = models.OneToOneField(User)
    facebook_id = models.BigIntegerField()
    access_token = models.CharField(max_length=150)

    def getFacebookProfile(self):
        fb_profile = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % self.access_token)

        return json.load(fb_profile)
