from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class HelpRequest(models.Model):
	HELPSTATE = (
		('unanswered', 'Unanswered'),
		('answered', 'Answered'),
		('clarification_required', 'Clarification Required'),
	)
	user = models.ForeignKey(User)
	question = models.TextField(blank=True, null=True)
	request_init = models.DateField(auto_now_add=True, null=True, blank=True)
	photo = models.ImageField(upload_to="help/img", null=True, blank=True)
	answer = models.TextField(blank=True, null=True)
	status = models.CharField(max_length=255, choices=HELPSTATE, default=(1,1))

	def __unicode__(self):
		return self.user.username


admin.site.register(HelpRequest)
