from django.db import models
from django.contrib.auth.models import User


class UserDailyReport(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateField(auto_now_add=True, null=True, blank=True)  # NOW
    modified = models.DateField(auto_now=True)  # auto update time


class DailyReport(models.Model):
    # a related pull should get the UserDailyReport list for the date
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    created = models.DateField(auto_now_add=True, null=True, blank=True)  # NOW
    modified = models.DateField(auto_now=True)  # auto update time

