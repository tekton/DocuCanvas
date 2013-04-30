from django import forms
from gapps.models import createUser


class UserForm(forms.ModelForm):
    admin_user = forms.CharField(max_length=100, help_text="Full email address of your admin account.")
    admin_pass = forms.CharField(widget=forms.PasswordInput(), max_length=100, help_text="Password of your admin account.")
    first_name = forms.CharField(max_length=100, help_text="New employee's first name.")
    last_name = forms.CharField(max_length=100, help_text="New employee's last name.")
    email_address = forms.CharField(max_length=100, help_text="Desired email address for new employee.")
    temp_pass = forms.CharField(max_length=100, help_text="Temporary password for new employee.")
    job_title = forms.CharField(max_length=100, help_text="New employee's job title.")
    extension = forms.CharField(max_length=100, help_text="New employee's extension.")
    mobile_number = forms.CharField(max_length=100, help_text="New employee's alternate contact number.")

    add_to_groups = forms.CharField(widget=forms.Textarea(), help_text="Separate by commas.  No need to include the 'everyone' group")

    class Meta:
        model = createUser
