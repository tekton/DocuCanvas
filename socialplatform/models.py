import json, urllib

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.files import File
import os


class FacebookProfile(models.Model):
	user = models.OneToOneField(User)
	facebook_id = models.CharField(max_length=150)
	profilePicture = models.ImageField(upload_to="upload/facebook", null=True, blank=True)
	image_url = models.URLField()
	access_token = models.CharField(max_length=255)
	helpdesk = models.NullBooleanField(default=True)
	notifications = models.NullBooleanField(default=True)
	active = models.NullBooleanField(default=True)

	def is_active(self):
		return active

	def deactivate(self):
		helpdesk = False
		notifications = False
		active = False
		self.save()

	def get_remote_image(self):
		if self.image_url and not self.profilePicture:
			result = urllib.urlretrieve(self.image_url)
			self.profilePicture.save(os.path.basename(self.image_url),File(open(result[0])))
			self.save()

	def update_token(self, token):
		self.access_token = token
		self.save()


class FBNotification(models.Model):
	sender = models.ForeignKey(User)
	fb_profile = models.ForeignKey(FacebookProfile)
	text = models.TextField()


class TwitterProfile(models.Model):
	user = models.ForeignKey(User)
	user_name = models.CharField(max_length=200)
	active = models.NullBooleanField(default=True)

	def Deactivate(self):
		active = False

	def Activate(self):
		active = True


class Tweet(models.Model):
	tweet_user = models.ForeignKey(User)
	content = models.CharField(max_length=140)
	created = models.DateField(auto_now_add=True)


class DMAll(models.Model):
	send_user = models.ForeignKey(User)
	content = models.CharField(max_length=140)
	created = models.DateField(auto_now_add=True)


class DMIndividual(models.Model):
	send_ind_user = models.ForeignKey(User)
	target_user = models.ForeignKey(TwitterProfile)
	content = models.CharField(max_length=140)
	created = models.DateField(auto_now_add=True)

admin.site.register(FacebookProfile)
admin.site.register(TwitterProfile)
admin.site.register(Tweet)
admin.site.register(DMAll)
admin.site.register(DMIndividual)