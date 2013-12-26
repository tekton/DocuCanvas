from django.db import models

# Create your models here.
class Sprint(models.Model):
	name = models.CharField(max_length=255)
	end = models.DateField()
	start = models.DateField()
	created = models.DateField(auto_now_add=True)
	modified = models.DateField(auto_now=True)