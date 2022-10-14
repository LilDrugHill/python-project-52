from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")
        widgets = {
            "first_name": forms.TextInput(),
            "last_name": forms.TextInput(),
            "username": forms.TextInput(),
            "password1": forms.PasswordInput(),
            "password2": forms.PasswordInput(),
        }

    def clean_username(self):  # User validator clean_[field]
        username = self.cleaned_data["username"]
        if len(username) > 12:
            raise ValidationError("Username is too long")

        return username


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")
        widgets = {
            "first_name": forms.TextInput(),
            "last_name": forms.TextInput(),
            "username": forms.TextInput(),
        }
