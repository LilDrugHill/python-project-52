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


class Logout(CustomLoginRequiredMixin, SuccessMessageMixin, LogoutView):
    success_message = gettext("You are logged out")
    template_name = 'auth/LogoutPage.html'
    login_url = reverse_lazy('home')


class UpdateUserData(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    success_message = gettext("User changed successfully")
    success_url = reverse_lazy("all_users")
    login_url = reverse_lazy("login")
    template_name = "auth/UpdatePage.html"
    form_class = UpdateRegUserForm
    model = User

    def post(self, request, pk, *args, **kwargs):
        if request.user.pk == pk:
            return super().post(self, request, pk, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, gettext("You are betrayer"))
            return redirect("all_users")

    def get(self, request, pk, *args, **kwargs):
        if request.user.pk == pk:
            return super().get(self, request, pk, *args, **kwargs)
        else:
            messages.add_message(request, messages.ERROR, gettext("You are betrayer"))
            return redirect("all_users")


class DeleteUser(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy("all_users")
    success_message = gettext("User deleted")
    template_name = "auth/DeletePage.html"
    login_url = reverse_lazy("login")

    def get(self, request, pk, *args, **kwargs):
        if pk == request.user.pk:
            if not request.user.author.count() and not request.user.executor.count():
                return super(DeleteUser, self).get(self, request, *args, **kwargs)

            messages.add_message(
                request,
                messages.ERROR,
                gettext("Cannot delete user because it's in use"),
            )
            return redirect(reverse_lazy("all_users"))
        else:
            messages.add_message(request, messages.ERROR, gettext("You are betrayer"))
            return redirect(reverse_lazy("all_users"))

    def post(self, request, pk, *args, **kwargs):
        if pk == request.user.pk:
            if not request.user.author.count() and not request.user.executor.count():
                return super(DeleteUser, self).post(self, request, *args, **kwargs)

            messages.add_message(
                request,
                messages.ERROR,
                gettext("Cannot delete user because it's in use"),
            )
            return redirect(reverse_lazy("all_users"))
        else:
            messages.add_message(request, messages.ERROR, gettext("You are betrayer"))
            return redirect(reverse_lazy("all_users"))
