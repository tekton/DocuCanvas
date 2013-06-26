from django.db import models
from django.contrib.auth.models import User


class TwitterProfile(models.Model):
	user = models.ForeignKey(User)
	user_name = models.CharField(max_length=200)
