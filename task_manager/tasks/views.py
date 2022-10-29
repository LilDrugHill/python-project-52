from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext

from task_manager.tasks.forms import TaskForm
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.models import TaskModel
from task_manager.utils import CustomLoginRequiredMixin


class ShowAllTasks(CustomLoginRequiredMixin, ListView):
    model = TaskModel
    template_name = "tasks/PageWithTasks.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {
            "filter": TaskFilter(
                self.request.GET, queryset=self.get_queryset(), request=self.request)
        }
        return dict(list(context.items()) + list(c_def.items()))


class ShowTask(CustomLoginRequiredMixin, DetailView):
    model = TaskModel
    context_object_name = "task"
    template_name = "tasks/Task.html"
    login_url = reverse_lazy("login")


class CreateTask(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm

    template_name = "tasks/CreationPage.html"
    success_url = reverse_lazy("all_tasks")
    login_url = reverse_lazy("login")
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
    login_url = reverse_lazy("login")


class DeleteTask(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
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
