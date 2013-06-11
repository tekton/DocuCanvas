from django import forms

from notifications.models import *
from django.forms.models import model_to_dict


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
