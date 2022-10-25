from django import forms
from task_manager.labels.models import LabelModel
from django.utils.translation import gettext


class LabelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)

    class Meta:
        model = LabelModel
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": gettext("Name"), "class": "form-control"}
            ),
        }
