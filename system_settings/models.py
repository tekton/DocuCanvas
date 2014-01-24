from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class SystemSetting(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    created_user = models.ForeignKey(User, null=True, blank=True, related_name='created_user')
    modified_user = models.ForeignKey(User, null=True, blank=True, related_name='modified_user')

    def __unicode__(self):
        return self.name


admin.site.register(SystemSetting)
