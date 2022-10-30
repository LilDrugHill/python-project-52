from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.utils.translation import gettext
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.utils import CustomLoginRequiredMixin
from task_manager.auth.forms import (
    UpdateRegUserForm,
    CustomAuthenticationForm,
)


class RegisterUser(SuccessMessageMixin, CreateView):
    form_class = UpdateRegUserForm
    template_name = "auth/SignUpPage.html"
    success_url = reverse_lazy("login")
    success_message = gettext("You have been successfully registered")


class LoginUser(SuccessMessageMixin, LoginView):
    form_class = CustomAuthenticationForm
    template_name = "auth/SignInPage.html"
    success_url = reverse_lazy("home")
    success_message = gettext("Successfully login")


class ShowAllUsers(ListView):
    model = User
    template_name = "auth/PageWithUsers.html"

    def get_queryset(self):
        return User.objects.filter(is_staff=False)


class Logout(LogoutView):
    success_message = gettext("You are logged out")
    login_url = reverse_lazy("home")
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.INFO, self.success_message)
        return redirect(self.success_url)


class UpdateUserData(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    success_message = gettext("User changed successfully")
    success_url = reverse_lazy("all_users")
    login_url = reverse_lazy("login")
    template_name = "auth/UpdatePage.html"
    form_class = UpdateRegUserForm
    model = User
    http_method_names = ["get", "post"]

    def dispatch(self, request, pk, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            if request.user.pk == pk:
                handler = getattr(
                    self, request.method.lower(), self.http_method_not_allowed
                )
            else:
                messages.add_message(
                    request, messages.ERROR, gettext("You are betrayer")
                )
                return redirect("all_users")
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class DeleteUser(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy("all_users")
    success_message = gettext("User deleted")
    template_name = "auth/DeletePage.html"
    login_url = reverse_lazy("login")
    http_method_names = ["get", "post"]

    def dispatch(self, request, pk, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            if pk == request.user.pk:
                if (
                    not request.user.author.exists()
                    and not request.user.executor.exists()
                ):
                    handler = getattr(
                        self, request.method.lower(), self.http_method_not_allowed
                    )
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        gettext("Cannot delete user because it's in use"),
                    )
                    return redirect(reverse_lazy("all_users"))
            else:
                messages.add_message(
                    request, messages.ERROR, gettext("You are betrayer")
                )
                return redirect(reverse_lazy("all_users"))
        else:
            handler = self.http_method_not_allowed

        return handler(request, *args, **kwargs)
