from django import forms
from tinymce.widgets import TinyMCE
from daily_reports.models import ReportGroup, DailyReport

class ReportForm(forms.Form):
    date = forms.DateField(widget=forms.HiddenInput)
    personalReport = forms.CharField(label="Report", widget=TinyMCE(attrs={'cols': 100, 'rows': 20, 'id': 'something'}))
    # globalReport = forms.CharField(widget=forms.Textarea)


class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport


class GroupForm(forms.ModelForm):
    class Meta:
        model = ReportGroup
