from django import forms
from django.forms.extras import widgets
from datetime import date

YEAR_CHOICES = range(2013, date.today().year + 1)


class ReportForm(forms.Form):
    date = forms.DateField(widget=forms.HiddenInput)
    goToDate = forms.DateField(widget=widgets.SelectDateWidget(years=YEAR_CHOICES))
    personalReport = forms.CharField(widget=forms.Textarea)
    # globalReport = forms.CharField(widget=forms.Textarea)
