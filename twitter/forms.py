from django import forms
from twitter.models import TwitterProfile, Tweet, DMAll, DMIndividual


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