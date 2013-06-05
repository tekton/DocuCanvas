from django import forms

from checklists.models import Checklist, ChecklistInstance, ChecklistTag, CheckListLayoutItems
from newsfeed.models import NewsFeedItem

'''
Forms for submitting bug reports and suggestions
'''
class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        #verbose_name = _('MODELNAME')
        #verbose_name_plural = _('MODELNAMEs')

    def save(self, user=None, *args, **kwargs):
        new_checklist = False
        if user:
            if not self.instance.pk:
                new_checklist = True
        super(ChecklistForm, self).save(*args, **kwargs)
        if user:
            try:
                news_feed_item = NewsFeedItem()
                news_feed_item.user = user
                news_feed_item.project = self.instance.project
                news_feed_item.checklist = self.instance
                if new_checklist:
                    news_feed_item.newsfeed_type = 'create_checklist'
                else:
                    news_feed_item.newsfeed_type = 'update_checklist'
                news_feed_item.save()
            except Exception, e:
                print e
        return self.instance

    def __unicode__(self):
        pass


class CheckListLayoutItemsForm(forms.ModelForm):
    class Meta:
        model = CheckListLayoutItems


class ChecklistInstanceForm(forms.ModelForm):
    class Meta:
        model = ChecklistInstance
        fields = ('title',)


class ChecklistInstanceFullForm(forms.ModelForm):
    class Meta:
        model = ChecklistInstance


class ChecklistTagForm(forms.ModelForm):
    class Meta:
        model = ChecklistTag
