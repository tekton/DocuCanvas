from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class AnonymousFeedback(models.Model):
	summary = models.CharField(max_length=255)
	feedback = models.TextField(blank=True, null=True)
	timestamp = models.DateField(auto_now=True)


class SignedFeedback(models.Model):
	user = models.ForeignKey(User)
	summary = models.CharField(max_length=255)
	feedback = models.TextField(blank=True, null=True)
	timestamp = models.DateField(auto_now=True)


admin.site.register(AnonymousFeedback)
admin.site.register(SignedFeedback)