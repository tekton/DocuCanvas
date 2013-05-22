from django import forms
from django.contrib.auth.models import User


class PermissionForm(forms.Form):

    view_users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)
    update_users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)
    delete_users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)
