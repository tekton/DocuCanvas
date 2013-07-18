from django import forms
from feedback.models import AnonymousFeedback, SignedFeedback


class AnonymousForm(forms.ModelForm):
	class Meta:
		model = AnonymousFeedback


class SignedForm(forms.ModelForm):
	class Meta:
		model = SignedFeedback