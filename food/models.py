from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.


class FoodRequest(models.Model):
    user = models.ForeignKey(User)
    item = models.CharField(max_length=255)



admin.site.register(FoodRequest)