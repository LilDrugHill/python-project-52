from .models import StatusModel
from task_manager.utils import DataMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect

from .forms import StatusForm


class ShowAllStatuses(DataMixin, LoginRequiredMixin, ListView):
    model = StatusModel
    template_name = "statuses/PageWithAll.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=gettext("All statuses page"),
            creation_title=gettext("Create status"),
            creation_page=reverse_lazy("create_status"),
            update_page="update_status",
            delete_page="delete_status",
            update_word=gettext("Update"),
            delete_word=gettext("Delete"),
        )
        return dict(list(context.items()) + list(c_def.items()))


class CreateStatus(DataMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StatusModel
    form_class = StatusForm

    template_name = "statuses/CreationPage.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("all_statuses")
    success_message = gettext("Status created")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=gettext("Status creation page"),
            creation_button=gettext("Create"),
        )
        return dict(list(context.items()) + list(c_def.items()))


class UpdateStatus(DataMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = StatusForm
    model = StatusModel

    template_name = "statuses/UpdatePage.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("all_statuses")
    success_message = gettext("Status updated")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=gettext("Update status page"), update_button=gettext("Update")
        )
        return dict(list(context.items()) + list(c_def.items()))


class DeleteStatus(DataMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = StatusModel
    success_message = gettext("Status deleted")
    success_url = reverse_lazy("all_statuses")
    template_name = "statuses/DeletePage.html"
    login_url = reverse_lazy("login")

    def post(self, request, pk, *args, **kwargs):
        if not self.get_object().taskmodel_set.exists():
            return super().post(self, request, *args, **kwargs)
        else:
            messages.add_message(
                request,
                messages.ERROR,
                gettext("Can't delete status because it's in use"),
            )
            return redirect(reverse_lazy("all_statuses"))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=gettext("Delete status page"))
        return dict(list(context.items()) + list(c_def.items()))
