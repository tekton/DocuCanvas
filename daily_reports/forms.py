from django import forms


class ReportForm(forms.Form):
    date = forms.DateField(widget=forms.HiddenInput)
    personalReport = forms.CharField(label="Report", widget=forms.Textarea)
    # globalReport = forms.CharField(widget=forms.Textarea)
