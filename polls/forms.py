from django import forms

from polls.models import Poll, PollItem, PollUser
from newsfeed.models import NewsFeedItem


class PollForm(forms.ModelForm):
	class Meta:
		model = Poll


class ItemForm(forms.ModelForm):
	class Meta:
		model = PollItem