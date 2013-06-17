from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    creator = models.ForeignKey(User)
    message = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    def __unicode__(self):
        return self.message


class NotificationRecipient(models.Model):
    user = models.ForeignKey(User)
    notification = models.ForeignKey(Notification)
    read = models.NullBooleanField(null=True, blank=True, default=False)
    created = models.DateField(auto_now_add=True)
    def __unicode__(self):
        return self.notification.message
