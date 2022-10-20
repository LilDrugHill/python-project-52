from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation


class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": gettext("Password"),
                "class": "form-control",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": gettext("Password confirmation"),
                "class": "form-control",
            }
        ),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")
        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": gettext("Name"), "class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": gettext("Last name"), "class": "form-control"}
            ),
            "username": forms.TextInput(
                attrs={"placeholder": gettext("Username"), "class": "form-control"}
            ),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")
        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": gettext("Name"), "class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": gettext("Name"), "class": "form-control"}
            ),
            "username": forms.TextInput(
                attrs={"placeholder": gettext("Name"), "class": "form-control"}
            ),
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label_suffix="",
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "placeholder": gettext("Username"),
                "class": "form-control",
            }
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": gettext("Password"),
                "class": "form-control",
            }
        ),
    )

    class Meta:
        proxy = True
