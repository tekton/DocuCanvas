from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class Poll(models.Model):
    creator = models.ForeignKey(User)
    total_items = models.IntegerField(default=2, null=True, blank=True)
    name = models.CharField(max_length=255)
    context = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateField(auto_now_add=True, null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    max_votes = models.IntegerField(default=1, null=True, blank=True)


class PollItem(models.Model):
    added_by = models.ForeignKey(User)
    poll = models.ForeignKey(Poll)
    item = models.CharField(max_length=255)
    votes = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateField(auto_now_add=True, null=True, blank=True)


class PollUser(models.Model):
    user = models.ForeignKey(User)
    poll = models.ForeignKey(Poll)
    ip = models.IPAddressField(blank=True, null=True)


admin.site.register(Poll)
admin.site.register(PollItem)
admin.site.register(PollUser)