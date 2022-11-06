from django import forms
from task_manager.tasks.models import TaskModel
from django.utils.translation import gettext_lazy as _


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)
        self.fields["status"].empty_label = _("Status not selected")
        self.fields["executor"].empty_label = _("Executor not selected")

    def __str__(self):
        return self.name

    class Meta:
        model = TaskModel
        fields = ("name", "description", "status", "executor", "labels")
        widgets = {
            "author": forms.HiddenInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "executor": forms.Select(attrs={"class": "form-control"}),
            "labels": forms.SelectMultiple(attrs={"class": "form-control"}),
        }
