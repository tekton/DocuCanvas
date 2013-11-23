from django import forms
from django.contrib.auth.models import User
from models import UserTemplates


class PermissionForm(forms.Form):
    view_users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)
    update_users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)
    delete_users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)


class UserTemplatesForm(forms.ModelForm):
    class Meta:
        model = UserTemplates
        exclude=['example_url']
