from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import DeleteView


class CustomLoginRequiredMixin(LoginRequiredMixin):
    permission_denied_message = gettext("You have to be logged in to access that page")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.WARNING, self.permission_denied_message
            )
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CustomDispatchChangeUserMixin:
    http_method_names = ["post", "get"]
    url_to_all = reverse_lazy("home")
    in_use_error_text = "set the error text using the 'in_use_error_text' attribute"

    def dispatch(self, request, pk, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            if pk == request.user.pk:
                handler = getattr(
                    self, request.method.lower(), self.http_method_not_allowed)
            else:
                messages.add_message(
                    request, messages.ERROR, gettext("You are betrayer")
                )
                return redirect(self.url_to_all)
        else:
            handler = self.http_method_not_allowed

        return handler(request, *args, **kwargs)


class SomeFuncsForTestsMixin:
    password = "Asdfg123456"

    def login_user(self, user):
        self.client.login(username=user.username, password=self.password)
