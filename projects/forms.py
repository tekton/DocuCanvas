from django import forms
from django.forms import ModelForm
from models import *
from newsfeed.models import *
from django.contrib.admin.widgets import AdminDateWidget


'''
Forms for submitting bug reports and suggestions
'''

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project

    def save(self, user=None, *args, **kwargs):
        new_project = False
        if user:
            if not self.instance.pk:
                new_project = True
        super(ProjectForm, self).save(*args, **kwargs)
        if user:
            if new_project:
                try:
                    news_feed_item = NewsFeedItem()
                    news_feed_item.user = user
                    news_feed_item.project = self.instance
                    news_feed_item.newsfeed_type = 'create_project'
                    news_feed_item.save()
                except Exception, e:
                    print(e)
            else:
                try:
                    news_feed_item = NewsFeedItem()
                    news_feed_item.user = user
                    news_feed_item.project = self.instance
                    news_feed_item.newsfeed_type = 'update_project'
                    news_feed_item.save()
                except Exception, e:
                    print(e)
        return self.instance
