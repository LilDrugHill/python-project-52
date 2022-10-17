from django import forms
from .models import LabelModel


class LabelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    class Meta:
        model = LabelModel
        fields = '__all__'
