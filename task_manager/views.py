from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.utils.translation import gettext
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import RegisterUserForm, UserUpdateForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .utils import DataMixin, menu


class HomePageView(DataMixin, TemplateView):
    template_name = "task_manager/base.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Home page")
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, SuccessMessageMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "task_manager/SignUpPage.html"
    success_url = reverse_lazy("home")
    success_message = gettext("You have been successfully registered")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Reg page")
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = "task_manager/SignInPage.html"
    success_url = reverse_lazy("home")
    success_message = gettext("Successfully login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=gettext("Login page"))
        return dict(list(context.items()) + list(c_def.items()))


class ShowAllUsers(DataMixin, ListView):
    model = User
    template_name = "task_manager/PageWithUsers.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=gettext("All users page"),
            update_word=gettext("Update"),
            delete_word=gettext("Delete"),
        )
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return User.objects.filter(is_staff=False)


def logout_user(request):
    logout(request)
    return redirect("home")


class UpdateUserData(DataMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    success_message = gettext("User data updated")
    success_url = reverse_lazy("home")
    login_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            update_session_auth_hash(request, request.user)
            return redirect("home")
        else:
            return render(
                request,
                "task_manager/UpdateUserPage.html",
                context={
                    "user_form": user_form,
                    "password_form": password_form,
                    "menu": menu,
                },
            )

    def get(self, request, pk, *args, **kwargs):
        if request.user.pk == pk:
            user_form = UserUpdateForm(
                initial={
                    "username": request.user.username,
                    "first_name": request.user.first_name,
                    "last_name": request.user.last_name,
                }
            )
            password_form = PasswordChangeForm(request.user)
        else:
            messages.add_message(request, messages.ERROR, "You are betrayer")
            return redirect("home")

        return render(
            request,
            "task_manager/UpdateUserPage.html",
            context={
                "user_form": user_form,
                "password_form": password_form,
                "menu": menu,
                "title": "Update user data page",
                "username": request.user.username,
            },
        )


class DeleteUser(DataMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy("home")
    success_message = gettext("User deleted")
    template_name = "DeletePage.html"
    login_url = reverse_lazy("login")

    def get(self, request, pk, *args, **kwargs):
        if pk == request.user.pk:
            if not request.user.author.count() and not request.user.executor.count():
                return super(DeleteUser, self).get(self, request, *args, **kwargs)
                
            messages.add_message(
                request,
                messages.ERROR,
                gettext("Cannot delete user because it is in use"),
            )
            return redirect(reverse_lazy("all_users"))
        else:
            messages.add_message(request, messages.ERROR, "You are betrayer")
            return redirect(reverse_lazy("home"))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Delete user page")
        return dict(list(context.items()) + list(c_def.items()))
