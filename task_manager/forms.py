from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


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


class CustomSetPasswordForm(forms.Form):
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": _("Password"),
            }
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-control",
                "placeholder": _("Password confirmation"),
            }
        ),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
