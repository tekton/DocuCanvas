from django import forms
from tinymce.widgets import TinyMCE

class ReportForm(forms.Form):
    date = forms.DateField(widget=forms.HiddenInput)
    personalReport = forms.CharField(label="Report", widget=TinyMCE(attrs={'cols': 50, 'rows': 20, 'id': 'something'}))
    # globalReport = forms.CharField(widget=forms.Textarea)
