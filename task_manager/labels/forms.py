from django import forms
from task_manager.labels.models import LabelModel
from django.utils.translation import gettext_lazy as _


class LabelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)

    class Meta:
        model = LabelModel
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": _("Name"), "class": "form-control"}
            ),
        }
