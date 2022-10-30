from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext


class CustomLoginRequiredMixin(LoginRequiredMixin):
    permission_denied_message = gettext("You have to be logged in to access that page")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(
                request, messages.WARNING, self.permission_denied_message
            )
            return self.handle_no_permission()
        return super(CustomLoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class CustomDispatchForDeletionMixin:
    http_method_names = [
        'post',
        'get'
    ]
    url_to_all = reverse_lazy('home')
    in_use_error_text = "set the error text using the 'in_use_error_text' attribute"

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            if request.method.lower() == 'post':
                if self.get_object().taskmodel_set.exists():
                    messages.add_message(
                        request,
                        messages.ERROR,
                        self.in_use_error_text)
                    return redirect(self.url_to_all)
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
