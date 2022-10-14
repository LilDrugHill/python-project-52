from django import forms
from .models import TaskModel
from django.utils.translation import gettext


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].empty_label = gettext("Status not selected")
        self.fields["executor"].empty_label = gettext("Executor not selected")

    def __str__(self):
        return self.name

    class Meta:
        model = TaskModel
        fields = ("name", "description", "status", "executor", "labels")
        widgets = {"author": forms.HiddenInput()}
