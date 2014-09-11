from django import forms

from checklists.models import Checklist, ChecklistInstance, ChecklistTag, CheckListLayoutItems
from newsfeed.models import NewsFeedItem
from django.forms.models import model_to_dict


'''
    Forms for submitting checklists
'''


class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        #verbose_name = _('MODELNAME')
        #verbose_name_plural = _('MODELNAMEs')

    '''
    def save(self, user=None, *args, **kwargs):
        new_checklist = False
        if user:
            if not self.instance.pk:
                new_checklist = True
            else:
                old_checklist = Checklist.objects.get(pk=self.instance.pk)
        super(ChecklistForm, self).save(*args, **kwargs)
        if user:
            try:
                news_feed_item = NewsFeedItem()
                news_feed_item.user = user
                news_feed_item.project = self.instance.project
                news_feed_item.checklist = self.instance
                if new_checklist:
                    news_feed_item.newsfeed_type = 'create_checklist'
                    news_feed_item.save()
                else:
                    try:
                        if old_checklist.name != self.instance.name:
                            news_feed_item.newsfeed_type = 'update_checklist'
                            news_feed_item.field_change = 'name'
                            news_feed_item.old_value = old_checklist.name
                            news_feed_item.new_value = self.instance.name
                            news_feed_item.save()
                        if old_checklist.project != self.instance.project:
                            news_feed_item.newsfeed_type = 'update_checklist'
                            news_feed_item.field_change = 'project'
                            news_feed_item.old_value = old_checklist.project
                            news_feed_item.new_value = self.instance.project
                            news_feed_item.save()
                    except Exception, e:
                        print(e)
            except Exception, e:
                print(e)
        return self.instance
    '''
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
