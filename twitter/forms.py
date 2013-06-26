from django import forms
from twitter.models import TwitterProfile


class TwitterForm(forms.ModelForm):
	class Meta:
		model = TwitterProfile
		fields = ('user', 'user_name')