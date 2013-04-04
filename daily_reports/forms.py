from django import forms
from django.forms import ModelForm
from models import *

'''
Forms for submitting bug reports and suggestions
'''


class DailyReportForm(forms.ModelForm):
    class Meta:
        model = UserDailyReport
