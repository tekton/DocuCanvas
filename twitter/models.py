from django.db import models
from django.contrib.auth.models import User


class TwitterProfile(models.Model):
	user = models.ForeignKey(User)
	user_name = models.CharField(max_length=200)
	oauth_token = models.CharField(max_length=200)
	oauth_secret = models.CharField(max_length=200)
