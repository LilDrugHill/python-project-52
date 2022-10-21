from django.db import models
from django.utils.translation import gettext


class LabelModel(models.Model):
    name = models.CharField(max_length=50, verbose_name=gettext("Name"))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=gettext("Creation date")
    )

    def __str__(self):
        return self.name
