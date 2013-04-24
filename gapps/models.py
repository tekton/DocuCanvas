from django.db import models

# Create your models here.

class createUser(models.Model):
	admin_user = models.CharField(max_length=100)
	admin_pass = models.CharField(max_length=100)

	first_name = models.CharField(max_length=100)
	last_name =  models.CharField(max_length=100)
	email_address = models.CharField(max_length=100)
	temp_pass = models.CharField(max_length=100)
	job_title = models.CharField(max_length=100)
	extension = models.CharField(max_length=100)
	mobile_number =models.CharField(max_length=100)
	add_to_groups = models.TextField(blank = True, null = True)

	def __unicode__(self):
		return self.email_address