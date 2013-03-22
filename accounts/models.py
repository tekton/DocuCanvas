from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Account(models.Model):
    user = models.ForeignKey(User)
    # Any "special" fields that a user should have should be added here...
    avatar = models.CharField(max_length=255, null=True, blank=True, default="/static/img/pony.png")
    git_account = models.CharField(max_length=255, null=True, blank=True)  # in case we have internal git servers
    github_account = models.CharField(max_length=255, null=True, blank=True)  # for all the people who use github
    location = models.CharField(max_length=255, null=True, blank=True)  # could be address, but could be "the office"
