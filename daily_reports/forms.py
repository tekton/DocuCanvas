from django.forms import ModelForm
from models import *

'''
Forms for submitting bug reports and suggestions
'''


class DailyReportForm(ModelForm):
    class Meta:
        model = UserDailyReport
        fields = ("date", "description", )
