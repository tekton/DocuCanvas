from django import forms
from helpdesknew.models import HelpRequest, HelpResponse


class HelpForm(forms.ModelForm):
	class Meta:
		model = HelpRequest
		fields = ('user', 'question', 'photo', 'name')

class AckForm(forms.ModelForm):
	class Meta:
		model = HelpRequest
		fields = ('user', 'ack_response', 'name')


class HelpFormResponse(forms.ModelForm):
	class Meta:
		model = HelpResponse
		fields = ('user', 'helprequest', 'response')


class ResponseFormValue(forms.ModelForm):
	class Meta:
		model = HelpResponse
		fields = ('user', 'helprequest', 'value')

'''
class HelpPhotoForm(forms.ModelForm):
	class Meta:
		model = HelpImageFile
		fields = ('helprequest', 'photo')
'''