from django import forms

from issues.models import *
from projects.models import Project
from customfields import *
from django.forms.models import model_to_dict
from newsfeed.models import *
from tinymce.widgets import TinyMCE
from accounts.models import Account


'''
Forms for submitting bug reports and suggestions
'''


class IssueForm(forms.ModelForm):
    # description = forms.CharField(widget=TinyMCE(attrs={'cols': 100, 'rows': 20, 'id': 'something'}), required=False)
    class Meta:
        model = Issue
        fields = ('project', 'summary', 'description', 'meta_issues', 'projected_start','projected_end', 'assigned_to', 'sprint')

    def save(self, user=None, *args, **kwargs):
        print "form save"
        super(IssueForm, self).save(*args, **kwargs)
        if user:
            try:
                news_feed_item = NewsFeedItem()
                news_feed_item.user = user
                news_feed_item.issue = self.instance
                news_feed_item.project = self.instance.project
                news_feed_item.newsfeed_type = 'create_issue'
                news_feed_item.save()
            except Exception, e:
                print e
        return self.instance
    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        if self.initial is not None:
            # print "there were initial values"
            if "project" in self.initial:
                if self.initial["project"] is not None:
                    self.fields['meta_issues'] = forms.ModelChoiceField(required=False, queryset=MetaIssue.objects.filter(project=self.initial["project"]))
            self.fields["assigned_to"] = forms.ModelChoiceField(required=False, queryset=Account.objects.filter(assignable=True).order_by('user__username'))

class IssueFullForm(forms.ModelForm):
    # description = forms.CharField(widget=TinyMCE(attrs={'cols': 50, 'rows': 20, 'id': 'something'}))

    class Meta:
        model = Issue

    def save(self, user=None, *args, **kwargs):
        if self.instance.pk:
            if user:
                try:
                    old_issue = Issue.objects.get(pk=self.instance.id)
                    for field in self.instance._meta.fields:
                        if getattr(self.instance, field.attname) != getattr(old_issue, field.attname):
                            try:
                                ### create issue field update object if field changed
                                issue_field_update = IssueFieldUpdate()
                                issue_field_update.issue = self.instance
                                issue_field_update.user = user
                                issue_field_update.field = field.attname
                                issue_field_update.old_value = getattr(old_issue, field.attname)
                                issue_field_update.new_value = getattr(self.instance, field.attname)
                                issue_field_update.save()
                            except Exception, e:
                                print 'couldnt save status update'
                                print e

                            ### create issue status update object if status changed
                            if field.attname == 'status':
                                if self.instance.status != old_issue.status:
                                    try:
                                        issue_status_update = IssueStatusUpdate()
                                        issue_status_update.issue = self.instance
                                        issue_status_update.user = user
                                        issue_status_update.old_status = old_issue.status
                                        issue_status_update.new_status = self.instance.status
                                        issue_status_update.save()
                                    except Exception, e:
                                        print 'couldnt save status update'
                                        print e

                            if getattr(self.instance, field.attname) != '' and getattr(old_issue, field.attname) != '':
                                try:
                                    news_feed_item = NewsFeedItem()
                                    news_feed_item.user = user
                                    news_feed_item.issue = self.instance
                                    news_feed_item.project = self.instance.project
                                    news_feed_item.field_change = field.attname
                                    news_feed_item.old_value = getattr(old_issue, field.attname)
                                    news_feed_item.new_value = getattr(self.instance, field.attname)
                                    news_feed_item.newsfeed_type = 'update_issue'
                                    news_feed_item.save()
                                except Exception, e:
                                    print e
                except Exception, e:
                    print 'couldnt get old issue'
                    print e

            ### create historical issue object based on this new change
            try:
                issue_historical = IssueHistorical()
                issue_historical.issue = self.instance
                for field in self.instance._meta.fields:
                    if field.attname != 'id':
                        setattr(issue_historical, field.attname, getattr(self.instance, field.attname))
                issue_historical.save()
            except Exception, e:
                'couldnt save historical issue'
                print e

        super(IssueFullForm, self).save(*args, **kwargs)
        return self.instance


class CommentForm(forms.ModelForm):
    # description = forms.CharField(widget=TinyMCE(attrs={'cols': 50, 'rows': 20, 'id': 'something'}))

    class Meta:
        model = IssueComment

    def save(self, user=None, *args, **kwargs):
        if user:
            try:
                news_feed_item = NewsFeedItem()
                news_feed_item.user = user
                news_feed_item.issue = self.instance.issue
                news_feed_item.project = self.instance.issue.project
                news_feed_item.comment = self.instance.description
                news_feed_item.newsfeed_type = 'comment'
                news_feed_item.save()
            except Exception, e:
                print e
        super(CommentForm, self).save(*args, **kwargs)
        return self.instance


class MetaIssueForm(forms.ModelForm):
    # description = forms.CharField(widget=TinyMCE(attrs={'cols': 50, 'rows': 20, 'id': 'something'}))

    class Meta:
        model = MetaIssue


class AdvSearchForm(forms.Form):
    """
        TODO: move fields to init so they are actually dynamic
    """
    project = forms.ModelMultipleChoiceField(required=False, queryset=Project.objects.all())
    meta_issues = forms.ModelMultipleChoiceField(required=False, queryset=MetaIssue.objects.all())
    # state = forms.MultipleChoiceField(required=False, choices=models.BUGSTATE)
    # dates
    # projected_start = forms.DateField(required=False)
    # projected_end = forms.DateField(required=False)
    # actual_start = forms.DateField(required=False)
    # actual_end = forms.DateField(required=False)

    # date_reported = forms.DateField(required=False)

    # created = forms.DateField(required=False)
    # modified = forms.DateField(required=False)

    # view_type = forms.CharField(required=False)
    # link_slug = forms.SlugField(required=False)
    # screen_shot = forms.CharField(required=False)
    # wireframe = forms.CharField(required=False)
    # uri_to_test = forms.CharField(required=False)
    assigned_to = forms.ModelMultipleChoiceField(required=False, queryset=Account.objects.filter(assignable=True))
    created_by = forms.ModelMultipleChoiceField(required=False, queryset=Account.objects.filter(assignable=True))
    issue_type = forms.MultipleChoiceField(required=False, choices=ISSUETYPE)

    title = MultipleTextField(required=False)
    summary = MultipleTextField(required=False)
    description = MultipleTextField(required=False)
    # description = MultipleTextField(required=False, widget=MultipleTextarea)

    status = forms.MultipleChoiceField(required=False, choices=BUGSTATE)
    criticality = forms.MultipleChoiceField(required=False, choices=[(1, 'One'), (2, "Two"), (3, "Three")])
    priority = forms.MultipleChoiceField(required=False, choices=[(1, 'One'), (2, "Two"), (3, "Three")])
    fixability = forms.MultipleChoiceField(required=False, choices=[(1, 'One'), (2, "Two"), (3, "Three")])

    # r_and_d = MultipleTextField(required=False)
    # feature = MultipleTextField(required=False)
    os = MultipleTextField(label="Operating System", required=False)
    os_version = MultipleTextField(label="OS Version", required=False)
    browser = MultipleTextField(required=False)
    browser_version = MultipleTextField(required=False)
    
    created_start = forms.DateField(required=False)
    created_stop = forms.DateField(required=False)
    modified_start = forms.DateField(required=False)
    modified_stop = forms.DateField(required=False)


class TestForm(forms.ModelForm):
    # description = forms.CharField(widget=TinyMCE(attrs={'cols': 50, 'rows': 20, 'toolbar': 'undo redo textcolor'}))

    class Meta:
        model = Issue
