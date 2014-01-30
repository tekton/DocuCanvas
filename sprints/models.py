from django.db import models
from django.contrib import admin

# Create your models here.
class Sprint(models.Model):
	name = models.CharField(max_length=255)
	end = models.DateField()
	start = models.DateField()
	created = models.DateField(auto_now_add=True)
	modified = models.DateField(auto_now=True)
	validAssignable = models.NullBooleanField(default=True, blank=True, null=True)

	def __unicode__(self):
		return self.name


admin.site.register(Sprint)