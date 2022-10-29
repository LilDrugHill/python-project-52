from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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
