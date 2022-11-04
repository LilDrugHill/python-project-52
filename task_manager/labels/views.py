from django.contrib import messages
from django.shortcuts import redirect

from .models import LabelModel
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.labels.forms import LabelForm
from task_manager.utils import CustomLoginRequiredMixin, CustomDispatchForDeletionMixin


class ShowAllLabels(CustomLoginRequiredMixin, ListView):
    model = LabelModel
    template_name = "labels/PageWithAll.html"
    login_url = reverse_lazy("login")


class CreateLabel(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = LabelModel
    form_class = LabelForm

    template_name = "labels/CreationPage.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("all_labels")
    success_message = gettext("Label created")


class UpdateLabel(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = LabelModel
    form_class = LabelForm

    template_name = "labels/UpdatePage.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("all_labels")
    success_message = gettext("Label updated")


class DeleteLabel(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = LabelModel
    success_message = gettext("Label deleted")
    success_url = reverse_lazy("all_labels")
    template_name = "labels/DeletePage.html"
    login_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        if self.get_object().taskmodel_set.exists():
            messages.add_message(
                request, messages.ERROR, gettext("Can't delete label because it's in use")
            )
            return redirect(self.success_url)
        else:
            return super().post(self, request, *args, **kwargs)
