from django import forms
from datetime import date
from models import *

YEAR_CHOICES = range(2013, date.now().year + 1)


class ReportForm(forms.Form):
    date = forms.DateField(widget=forms.HiddenInput)
    goToDate = forms.DateField(widget=forms.SelectDateWidget(years=YEAR_CHOICES))
    personalReport = forms.CharField(widget=forms.Textarea)
    # globalReport = forms.CharField(widget=forms.Textarea)
