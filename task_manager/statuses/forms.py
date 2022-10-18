from django import forms
from .models import StatusModel
from django.utils.translation import gettext


class StatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)

    class Meta:
        model = StatusModel
        fields = ("name",)
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": gettext("Name"),
                                           "class": "form-control"}),

        }

