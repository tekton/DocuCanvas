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
    google_plus = models.CharField(max_length=255, null=True, blank=True)  #
    facebook = models.CharField(max_length=255, null=True, blank=True)  #
    twitter = models.CharField(max_length=255, null=True, blank=True)  #
    organization = models.CharField(max_length=255, null=True, blank=True)  #


class GoogleAccount(models.Model):
    """
        Google Account table to allow people to link 1 to unlimited Google/YouTube account to their account
    """
    user = models.ForeignKey(User)
    account = models.ForeignKey(Account)
    security_token = models.CharField(max_length=255, null=True, blank=True)
    # put other fields needed below ?
