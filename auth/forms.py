from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
# from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    # video = forms.CharField(label="Video")

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("A user with that email address already exists.")

    def save(self):
        user = super(RegisterForm, self).save(commit=False)
        user.is_active = True
#        # Launch thread to send email to the user.
#        thread = Thread(target=send_activation,  args=[user])
#        thread.setDaemon(True)
#        thread.start()
        user.save()

    class Meta:
        model = User
        fields = ("username", "email")  # , "video")


class EditAccountForm(PasswordChangeForm):
    class Meta:
        model = User
    # email = forms.CharField(max_length=255)
    # old_password = forms.CharField(max_length=255)
    # password1 = forms.CharField(max_length=255)
    # password2 = forms.CharField(max_length=255)
