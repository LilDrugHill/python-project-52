from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.utils.translation import gettext


class CustomLoginRequiredMixin(LoginRequiredMixin):
    must_login_message = gettext("You have to be logged in to access that page")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.WARNING, self.must_login_message)
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CustomHandleNoPermissionWithoutForbidden:
    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.add_message(
                self.request, messages.ERROR, self.permission_denied_message
            )
            return redirect(self.success_url)
        return redirect_to_login(
            self.request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name(),
        )


class SomeFuncsForTestsMixin:
    password = "Asdfg123456"

    def login_user(self, user):
        self.client.login(username=user.username, password=self.password)


class CustomUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().pk == self.request.user.pk
