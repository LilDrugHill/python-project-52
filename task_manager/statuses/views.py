from .models import StatusModel
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.statuses.forms import StatusForm
from task_manager.utils import CustomLoginRequiredMixin, CustomDispatchForDeletionMixin


class ShowAllStatuses(CustomLoginRequiredMixin, ListView):
    model = StatusModel
    template_name = "statuses/PageWithAll.html"
    login_url = reverse_lazy("login")


class CreateStatus(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StatusModel
    form_class = StatusForm

    template_name = "statuses/CreationPage.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("all_statuses")
    success_message = gettext("Status created")


class UpdateStatus(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = StatusForm
    model = StatusModel

    template_name = "statuses/UpdatePage.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("all_statuses")
    success_message = gettext("Status updated")


class DeleteStatus(
    CustomDispatchForDeletionMixin,
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = StatusModel
    success_message = gettext("Status deleted")
    success_url = reverse_lazy("all_statuses")
    template_name = "statuses/DeletePage.html"
    login_url = reverse_lazy("login")
    url_to_all = reverse_lazy("all_statuses")
    in_use_error_text = gettext("Can't delete status because it's in use")
    http_method_names = ["post", "get"]
