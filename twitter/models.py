from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class TwitterProfile(models.Model):
	user = models.ForeignKey(User)
	user_name = models.CharField(max_length=200)


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


admin.site.register(TwitterProfile)
admin.site.register(Tweet)
admin.site.register(DMAll)
admin.site.register(DMIndividual)