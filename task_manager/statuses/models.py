from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusModel(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_("Name"),
        unique=True,
        error_messages={"unique": _("Status with the same name already exists")},
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Creation date")
    )

    def __str__(self):
        return self.name
