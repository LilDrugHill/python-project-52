from .models import TaskModel
from task_manager.utils import DataMixin
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext

from .forms import TaskForm
from .filters import TaskFilter


class ShowAllTasks(DataMixin, LoginRequiredMixin, ListView):
    model = TaskModel
    template_name = "tasks/PageWithTasks.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=gettext("All tasks page"),
            creation_title=gettext("Create task"),
            creation_page=reverse_lazy("create_task"),
            update_page="update_task",
            delete_page="delete_task",
            update_word=gettext("Update"),
            delete_word=gettext("Delete"),
            filter=TaskFilter(
                self.request.GET, queryset=self.get_queryset(), request=self.request
            ),
            table_words={
                "id": gettext("ID"),
                "name": gettext("Name"),
                "status": gettext("Status"),
                "author": gettext("Author"),
                "executor": gettext("Executor"),
                "created_at": gettext("Creation date"),
            },
        )
        return dict(list(context.items()) + list(c_def.items()))


class ShowTask(DataMixin, LoginRequiredMixin, DetailView):
    model = TaskModel
    context_object_name = "task"
    template_name = "tasks/Task.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=gettext("Task view"),
            update_page="update_task",
            delete_page="delete_task",
        )
        return dict(list(context.items()) + list(c_def.items()))


class CreateTask(DataMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm

    template_name = "tasks/CreationPage.html"
    success_url = reverse_lazy("all_tasks")
    login_url = reverse_lazy("login")
    success_message = gettext("Task created")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=gettext("Creation task page"), creation_button=gettext("Create")
        )
        return dict(list(context.items()) + list(c_def.items()))


class UpdateTask(DataMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TaskModel
    form_class = TaskForm

    template_name = "tasks/UpdatePage.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("all_tasks")
    success_message = gettext("Task updated")
    login_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=gettext("Update task page"), update_button=gettext("Update")
        )
        return dict(list(context.items()) + list(c_def.items()))


class DeleteTask(DataMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TaskModel
    success_url = reverse_lazy("all_tasks")
    template_name = "tasks/DeletePage.html"
    success_message = gettext("Task deleted")
    login_url = reverse_lazy("login")

    def get(self, request, pk, *args, **kwargs):
        if request.user.pk == TaskModel.objects.get(pk=pk).author.pk:
            return super().get(self, request, *args, **kwargs)
        messages.add_message(
            request,
            messages.ERROR,
            f"{gettext('A task can only be deleted by its author.')}",
        )
        return redirect(reverse_lazy("all_tasks"))

    def post(self, request, pk, *args, **kwargs):
        if request.user.pk == TaskModel.objects.get(pk=pk).author.pk:
            return super().post(self, request, *args, **kwargs)
        messages.add_message(
            request,
            messages.ERROR,
            gettext("A task can only be deleted by its author."),
        )
        return redirect(reverse_lazy("all_tasks"))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=gettext("Delete task page"))
        return dict(list(context.items()) + list(c_def.items()))
