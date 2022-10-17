from django import forms
from .models import StatusModel


class StatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)

    class Meta:
        model = StatusModel
        fields = "__all__"
