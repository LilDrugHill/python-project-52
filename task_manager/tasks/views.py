from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext
from django_filters.views import FilterView

from task_manager.tasks.forms import TaskForm
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.models import TaskModel
from task_manager.utils import CustomLoginRequiredMixin


class ShowAllTasks(CustomLoginRequiredMixin, FilterView):
    model = TaskModel
    template_name = "tasks/PageWithTasks.html"
    login_url = reverse_lazy("login")
    filterset_class = TaskFilter


class ShowTask(CustomLoginRequiredMixin, DetailView):
    model = TaskModel
    context_object_name = "task"
    template_name = "tasks/Task.html"
    login_url = reverse_lazy("login")


class CreateTask(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm

    template_name = "tasks/CreationPage.html"
    success_url = reverse_lazy("all_tasks")
    success_message = gettext("Task created")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdateTask(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TaskModel
    form_class = TaskForm

    template_name = "tasks/UpdatePage.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("all_tasks")
    success_message = gettext("Task updated")


class DeleteTask(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TaskModel
    success_url = reverse_lazy("all_tasks")
    template_name = "tasks/DeletePage.html"
    success_message = gettext("Task deleted")
    login_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk == self.get_object().author.pk:
            return super(DeleteTask, self).dispatch(request, *args, **kwargs)
        else:
            messages.add_message(
                request,
                messages.ERROR,
                f"{gettext('A task can only be deleted by its author.')}",
            )
            return redirect(self.success_url)
