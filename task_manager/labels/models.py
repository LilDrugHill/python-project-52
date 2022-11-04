from django.db import models
from django.utils.translation import gettext


class LabelModel(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name=gettext("Name"),
                            unique=True,
                            error_messages={'unique': gettext("Label with the same name already exists")}
                            )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=gettext("Creation date")
    )

    def __str__(self):
        return self.name
