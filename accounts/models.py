from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from south.modelsinspector import add_introspection_rules

from oauth2client.django_orm import CredentialsField

class RecordPermissionManager(models.Manager):

    def get_for_model(self, model):
        try:
            key = model.pk
        except NameError:
            raise TypeError('Not a valid model')

        if key is None:
            raise ValueError('Model must already be persisted to the database')

        if type(key) is not int:
            raise TypeError("Model must have an integer primary key")

        cType = ContentType.objects.get_for_model(model.__class__)

        return self.filter(contentType=cType, recordID=key)

    def get_for_model_user(self, model, user, save_new=False):
        try:
            key = model.pk
        except NameError:
            raise TypeError('Not a valid model')

        if key is None:
            raise ValueError('Model must already be persisted to the database')

        if type(key) is not int:
            raise TypeError("Model must have an integer primary key")

        cType = ContentType.objects.get_for_model(model.__class__)

        if save_new:
            perm, created = self.get_or_create(contentType=cType, user=user, recordID=key)
        else:
            try:
                perm = self.get(contentType=cType, user=user, recordID=key)
            except RecordPermission.DoesNotExist:
                perm = RecordPermission()
                perm.contentType = cType
                perm.user = user
                perm.recordID = key

        return perm


class RecordPermission(models.Model):

    contentType = models.ForeignKey(ContentType)
    user = models.ForeignKey(User)
    recordID = models.PositiveIntegerField()
    record = GenericForeignKey("contentType", "recordID")
    canView = models.BooleanField(default=False)
    canUpdate = models.BooleanField(default=False)
    canDelete = models.BooleanField(default=False)

    # These are unused for now, added for future use
    viewableFields = models.CharField(max_length=255, default="", blank=True)
    updatableFields = models.CharField(max_length=255, default="", blank=True)

    objects = RecordPermissionManager()

    class Meta:
        unique_together = (('contentType', 'user', 'recordID'),)


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
    assignable = models.NullBooleanField(null=True, blank=True)

    def __unicode__(self):
        return self.user.username


class UserTemplates(models.Model):
    user = models.ForeignKey(User)
    viewName = models.CharField(max_length=255)  # it's possible this could just be a dropdown for the supported views, but we may as well enable them all as possible
    example_url = models.CharField(max_length=255, null=True, blank=True)
    pathToTemplate = models.CharField(max_length=255)  # this is relative to template- should add a "users upload section"

    def __unicode__(self):
        return "{} :: {}".format(self.user.username, self.viewName)

    class Meta:
        unique_together = (('user', 'viewName'),)


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


class AccountSetting(models.Model):
    user = models.ForeignKey(User)
    setting_name = models.CharField(max_length=255)
    setting_value = models.CharField(max_length=255, null=True, blank=True)
    # the fun parts...
    created = models.DateField(auto_now_add=True, null=True, blank=True)    # NOW
    modified = models.DateField(auto_now=True)                              # auto update time
    class Meta:
        unique_together = (('user', 'setting_name'),)


add_introspection_rules([], ["^oauth2client\.django_orm\.CredentialsField"])


admin.site.register(GoogleAccount)
admin.site.register(RecordPermission)
# admin.site.register(Account)
