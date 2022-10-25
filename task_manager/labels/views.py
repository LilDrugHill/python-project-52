from .models import LabelModel
from task_manager.utils import DataMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext
from django.contrib.messages.views import SuccessMessageMixin

from .forms import LabelForm


class ShowAllLabels(DataMixin, LoginRequiredMixin, ListView):
    model = LabelModel
    template_name = "labels/PageWithAll.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=gettext("All labels page"),
            creation_title=gettext("Create label"),
            creation_page=reverse_lazy("create_label"),
            update_page="update_label",
            delete_page="delete_label",
            update_word=gettext("Update"),
            delete_word=gettext("Delete"),
        )
        return dict(list(context.items()) + list(c_def.items()))


class CreateLabel(DataMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = LabelModel
    form_class = LabelForm

    template_name = "labels/CreationPage.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("all_labels")
    success_message = gettext("Label created")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=gettext("Label creation page"),
            creation_button=gettext("Create"),
        )
        return dict(list(context.items()) + list(c_def.items()))


class UpdateLabel(DataMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = LabelModel
    form_class = LabelForm

    template_name = "labels/UpdatePage.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("all_labels")
    success_message = gettext("Label updated")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title=gettext("Update label page"), update_button=gettext("Update")
        )
        return dict(list(context.items()) + list(c_def.items()))


class DeleteLabel(DataMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = LabelModel
    success_message = gettext("Label deleted")
    success_url = reverse_lazy("all_labels")
    template_name = "labels/DeletePage.html"
    login_url = reverse_lazy("login")

    def post(self, request, pk, *args, **kwargs):
        if not self.get_object().taskmodel_set.exists():
            return super().post(self, request, *args, **kwargs)
        else:
            messages.add_message(
                request,
                messages.ERROR,
                gettext("Can't delete label because it's in use"),
            )
            return redirect(reverse_lazy("all_labels"))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=gettext("Delete label page"))
        return dict(list(context.items()) + list(c_def.items()))
