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

admin.site.register(FacebookProfile)