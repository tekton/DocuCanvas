from django import forms
from socialplatform.models import TwitterProfile, Tweet, DMAll, DMIndividual, FacebookProfile


class TwitterForm(forms.ModelForm):
	class Meta:
		model = TwitterProfile
		fields = ('user', 'user_name')


class TweetForm(forms.ModelForm):
	class Meta:
		model = Tweet
		fields = ('tweet_user', 'content')


class DMAForm(forms.ModelForm):
	class Meta:
		model = DMAll
		fields = ('send_user', 'content')


class DMIForm(forms.ModelForm):
	class Meta:
		model = DMIndividual
		fields = ('send_ind_user', 'target_user', 'content')


class FacebookPermissions(forms.ModelForm):
	class Meta:
		model = FacebookProfile
		fields = ('helpdesk', 'notifications')