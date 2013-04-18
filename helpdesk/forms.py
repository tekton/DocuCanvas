from django import forms
from helpdesk.models import HelpRequest


class HelpForm(forms.ModelForm):
	class Meta:
		model = HelpRequest
		fields = ('user', 'question', 'photo')


class HelpFormComplete(forms.ModelForm):
	class Meta:
		model = HelpRequest