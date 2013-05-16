from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class HelpRequest(models.Model):
	help_state = (
		('no_response', 'No Responses'),
		('active', 'Active Responses'),
		('resolved', 'Resolved'),
		('reopened', 'Re-Opened'),
		('closed', 'Closed'),
	)
	user = models.ForeignKey(User)
	name = models.CharField(max_length=140)
	question = models.TextField(blank=True, null=True)
	request_init = models.DateField(auto_now_add=True, null=True, blank=True)
	photo = models.ImageField(upload_to="help/img", null=True, blank=True)
	status = models.CharField(max_length=255, choices=help_state, default=(1, 1))
	edit_status_bool = models.NullBooleanField(default=False)
	ack_response = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return self.user.username

	def update_status(self, n):
		print "updating status"
		if n == 1:
			self.status = self.help_state[1]
		elif n==3:
			self.status = self.help_state[3]
			self.ack_response = ""
		elif n==2:
			self.status = self.help_state[2]
		elif n==4:
			self.status = self.help_state[4]
		else:
			self.status = self.help_state[1]
		print "status updated"

	def question_is_edit(self):
		self.edit_status_bool = True


class HelpResponse(models.Model):
	response_value = (
		('input', 'Input'),
		('answer', 'Answer'),
	)
	user = models.ForeignKey(User)
	helprequest = models.ForeignKey(HelpRequest)
	response = models.TextField(blank=True, null=True)
	created = models.DateField(auto_now_add=True, null=True, blank=True)
	value = models.CharField(max_length=255, choices=response_value, default=(1, 1))

	def __unicode__(self):
		return self.user.username

	def mark_answer(self):
		self.value = self.response_value[1]
		print "response set as answer"

	def mark_input(self):
		self.value = self.response_value[0]
		print "response set as input"

'''
class HelpImageFile(models.Model):
	helprequest = models.ForeignKey(HelpRequest, null=True, blank=True)
	photo = models.ImageField(upload_to="help/img", null=True, blank=True)
'''

admin.site.register(HelpRequest)
admin.site.register(HelpResponse)

