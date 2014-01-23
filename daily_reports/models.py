from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class UserDailyReport(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateField(auto_now_add=True, null=True, blank=True)  # NOW
    modified = models.DateField(auto_now=True)  # auto update time

    def __unicode__(self):
        return "{} :: {}".format(self.user, self.date)


class DailyReport(models.Model):
    # a related pull should get the UserDailyReport list for the date
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    created = models.DateField(auto_now_add=True, null=True, blank=True)  # NOW
    modified = models.DateField(auto_now=True)  # auto update time


class ReportGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


class GroupMember(models.Model):
    group = models.ForeignKey(ReportGroup)
    user = models.ForeignKey(User)


admin.site.register(UserDailyReport)
admin.site.register(ReportGroup)
admin.site.register(GroupMember)