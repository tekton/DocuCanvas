from django import forms

from issues.models import *
from projects.models import Project
from customfields import *

'''
Forms for submitting bug reports and suggestions
'''


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('project', 'summary', 'description')


class IssueFullForm(forms.ModelForm):
    class Meta:
        model = Issue


class CommentForm(forms.ModelForm):
    class Meta:
        model = IssueComment


class MetaIssueForm(forms.ModelForm):
    class Meta:
        model = MetaIssue


class AdvSearchForm(forms.Form):
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

    assigned_to = forms.ModelMultipleChoiceField(required=False, queryset=User.objects.all())
    issue_type = forms.MultipleChoiceField(required=False, choices=ISSUETYPE)

    title = MultipleTextField(required=False)
    summary = MultipleTextField(required=False)
    description = MultipleTextField(required=False)
    # description = MultipleTextField(required=False, widget=MultipleTextarea)

    status = forms.MultipleChoiceField(required=False, choices=BUGSTATE)
    criticality = forms.MultipleChoiceField(required=False, choices=[(1, 'One'), (2, "Two"), (3, "Three")])
    priority = forms.MultipleChoiceField(required=False, choices=[(1, 'One'), (2, "Two"), (3, "Three")])
    fixability = forms.MultipleChoiceField(required=False, choices=[(1, 'One'), (2, "Two"), (3, "Three")])

    r_and_d = MultipleTextField(required=False)
    feature = MultipleTextField(required=False)
    os = MultipleTextField(label="Operating System", required=False)
    os_version = MultipleTextField(label="OS Version", required=False)
    browser = MultipleTextField(required=False)
    browser_version = MultipleTextField(required=False)
