from django.views.generic.base import TemplateView, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from .forms import RegisterUserForm, UserUpdateForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required


menu = [
    {'title': 'All users', 'url_name': 'all_users'},
    {'title': 'Home', 'url_name': 'home'},
]


class HomePageView(TemplateView):

    def greetings(request, messages=messages):
        return render(request, 'task_manager/base.html', context={
            'project_name': gettext('Task manager'),
            'greeting_massage': gettext('My simple hexlet-project, where you can manage your tasks'),
            'test_string': None,
            'message': messages.get_messages(request),
            'menu': menu
        })


class UserPage(TemplateView):

    def get_users(request):
        return render()


    def clear_table(request):
        User.objects.all().delete()
        messages.add_message(request, messages.INFO, 'Table is clear')
        return redirect('HomePage')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'task_manager/SignUpPage.html'
    success_url = reverse_lazy('home')
    success_message = 'Success'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


class LoginUser(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'task_manager/signinpage.html'
    success_url = reverse_lazy('home')
    success_message = 'Successfully login'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


class ShowAllUsers(ListView):
    model = User
    template_name = 'task_manager/PageWithUsers.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

    def get_queryset(self):
        return User.objects.filter(is_staff=False)


def logout_user(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def update_user_data(request, pk):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            update_session_auth_hash(request, request.user)
            return redirect('home')
        else:
            return render(request, 'task_manager/UpdateUserPage.html', context={
                'user_form': user_form,
                'password_form': password_form,
                'menu': menu
            })

    else:
        if request.user.pk == pk:
            user_form = UserUpdateForm()
            password_form = PasswordChangeForm(request.user)
        else:
            messages.add_message(request, messages.ERROR, 'You are betrayer')
            return redirect('home')

    return render(request, 'task_manager/UpdateUserPage.html', context={
        'user_form': user_form,
        'password_form': password_form,
        'menu': menu
    })


@login_required(login_url='login')
def delete_user(request, pk):
    if pk == request.user.pk:
        logout(request)
        User.objects.get(pk=pk).delete()
        messages.add_message(request, messages.INFO, 'User successfully deleted')
        return redirect('home')
    else:
        messages.add_message(request, messages.ERROR, 'You are betrayer')
        return redirect('home')
