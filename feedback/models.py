from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class AnonymousFeedback(models.Model):
	feedback = models.TextField(blank=True, null=True)
	timestamp = models.DateField(auto_now=True)


class SignedFeedback(models.Model):
	user = models.ForeignKey(User)
	feedback = models.TextField(blank=True, null=True)
	timestamp = models.DateField(auto_now=True)


class Feedback(models.Model):
	user = models.ForeignKey(User)
	feedback = models.TextField()
	created = models.DateField(auto_now_add=True)
	page = models.CharField(max_length=255)


admin.site.register(AnonymousFeedback)
admin.site.register(SignedFeedback)