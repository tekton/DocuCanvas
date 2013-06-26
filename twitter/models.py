from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class TwitterProfile(models.Model):
	user = models.ForeignKey(User)
	user_name = models.CharField(max_length=200)


admin.site.register(TwitterProfile)