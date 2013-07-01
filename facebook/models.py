import json, urllib

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class FacebookProfile(models.Model):
	user = models.OneToOneField(User)
	facebook_id = models.CharField(max_length=150)


class FBNotification(models.Model):
	sender = models.ForeignKey(User)
	fb_profile = models.ForeignKey(FacebookProfile)
	text = models.TextField()
