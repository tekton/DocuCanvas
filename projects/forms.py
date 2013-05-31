from django import forms
from django.forms import ModelForm
from models import *
from newsfeed.models import *


'''
Forms for submitting bug reports and suggestions
'''

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project

    def save(self, user=None, *args, **kwargs):
        if user:
            if self.instance.pk:
                try:
                    news_feed_item = NewsFeedItem()
                    news_feed_item.user = user
                    news_feed_item.project = self.instance
                    news_feed_item.description = str(user.username) + ' edited project ' + str(self.instance.name)
                    news_feed_item.save()
                except Exception, e:
                    print e
            else:
                try:
                    news_feed_item = NewsFeedItem()
                    news_feed_item.user = user
                    news_feed_item.project = self.instance
                    news_feed_item.description = str(user.username) + ' made new project ' + str(self.instance.name)
                    news_feed_item.save()
                except Exception, e:
                    print e
        super(ProjectForm, self).save(*args, **kwargs)
        return self.instance
