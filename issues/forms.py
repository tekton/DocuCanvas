from django import forms

from issues.models import Issue, IssueComment


'''
Forms for submitting bug reports and suggestions
'''


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ('project', 'summary', 'description')


class CommentForm(forms.ModelForm):
    class Meta:
        model = IssueComment
