from django import forms
from tinymce.widgets import TinyMCE
from daily_reports.models import ReportGroup

class ReportForm(forms.Form):
    date = forms.DateField(widget=forms.HiddenInput)
    personalReport = forms.CharField(label="Report", widget=TinyMCE(attrs={'cols': 100, 'rows': 20, 'id': 'something'}))
    # globalReport = forms.CharField(widget=forms.Textarea)


class GroupForm(forms.ModelForm):
    class Meta:
        model = ReportGroup
