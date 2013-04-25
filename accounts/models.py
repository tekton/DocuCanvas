from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from south.modelsinspector import add_introspection_rules

from oauth2client.django_orm import CredentialsField

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
    account = models.ForeignKey(Account, null=True)
    google_account_id = models.CharField(max_length=255, null=True, blank=True) #id
    account_label = models.CharField(max_length=255, null=True, blank=True) #email address
    # refresh_token = models.CharField(max_length=255, null=True, blank=True)
    # client_auth_key = models.CharField(max_length=255, null=True, blank=True)
    # client_auth_key_expiration = models.DateTimeField(null=True, blank=True)
    credentials = CredentialsField()

add_introspection_rules([], ["^oauth2client\.django_orm\.CredentialsField"])

admin.site.register(GoogleAccount)
