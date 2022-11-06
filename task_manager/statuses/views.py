from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.statuses.forms import StatusForm
from task_manager.utils import CustomLoginRequiredMixin
from task_manager.statuses.models import StatusModel


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
    success_message = _("Status created")


class UpdateStatus(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = StatusForm
    model = StatusModel

    template_name = "statuses/UpdatePage.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("all_statuses")
    success_message = _("Status updated")


class DeleteStatus(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    model = StatusModel
    success_message = _("Status deleted")
    success_url = reverse_lazy("all_statuses")
    template_name = "statuses/DeletePage.html"
    login_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        if self.get_object().taskmodel_set.exists():
            messages.add_message(
                request,
                messages.ERROR,
                _("Can't delete status because it's in use"),
            )
            return redirect(self.success_url)
        else:
            return super(DeleteStatus, self).post(request, *args, **kwargs)
