from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin


from task_manager.utils import (
    CustomLoginRequiredMixin,
    CustomHandleNoPermissionWithoutForbidden,
    CustomUserPassesTestMixin,
)
from task_manager.auth.forms import (
    UpdateRegUserForm,
    CustomAuthenticationForm,
)


class RegisterUser(SuccessMessageMixin, CreateView):
    form_class = UpdateRegUserForm
    template_name = "auth/SignUpPage.html"
    success_url = reverse_lazy("login")
    success_message = _("You have been successfully registered")


class LoginUser(SuccessMessageMixin, LoginView):
    form_class = CustomAuthenticationForm
    template_name = "auth/SignInPage.html"
    success_url = reverse_lazy("home")
    success_message = _("Successfully login")


class ShowAllUsers(ListView):
    model = User
    template_name = "auth/PageWithUsers.html"

    def get_queryset(self):
        return User.objects.filter(is_staff=False)


class Logout(LogoutView):
    success_message = _("You are logged out")
    login_url = reverse_lazy("home")
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.INFO, self.success_message)
        return redirect(self.success_url)


class UpdateUserData(
    CustomLoginRequiredMixin,
    CustomHandleNoPermissionWithoutForbidden,
    CustomUserPassesTestMixin,
    SuccessMessageMixin,
    UpdateView,
):
    success_message = _("User changed successfully")
    success_url = reverse_lazy("all_users")
    login_url = reverse_lazy("login")
    template_name = "auth/UpdatePage.html"
    form_class = UpdateRegUserForm
    model = User
    permission_denied_message = _("You are betrayer")


class DeleteUser(
    CustomLoginRequiredMixin,
    CustomHandleNoPermissionWithoutForbidden,
    CustomUserPassesTestMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = User
    success_url = reverse_lazy("all_users")
    success_message = _("User deleted")
    template_name = "auth/DeletePage.html"
    login_url = reverse_lazy("login")
    permission_denied_message = _("You are betrayer")

    def post(self, request, *args, **kwargs):
        if (
            not self.get_object().author.exists()
            and not self.get_object().executor.exists()
        ):
            return super().post(request, *args, **kwargs)
        messages.add_message(
            request, messages.ERROR, _("Cannot delete user because it's in use")
        )
        return redirect(self.success_url)
