from django import forms
from task_manager.statuses.models import StatusModel
from django.utils.translation import gettext_lazy as _


class StatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)

    class Meta:
        model = StatusModel
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": _("Name"), "class": "form-control"}
            ),
        }
