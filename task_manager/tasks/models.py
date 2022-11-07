from django.db import models
from task_manager.statuses.models import StatusModel
from task_manager.auth.models import UserStr
from task_manager.labels.models import LabelModel
from django.utils.translation import gettext_lazy as _


class TaskModel(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    description = models.CharField(
        max_length=255, verbose_name=_("Description"), blank=True, null=True
    )
    status = models.ForeignKey(
        StatusModel, on_delete=models.PROTECT, verbose_name=_("Status")
    )
    author = models.ForeignKey(
        UserStr,
        related_name="author",
        on_delete=models.PROTECT,
        verbose_name=_("Author"),
    )
    executor = models.ForeignKey(
        UserStr,
        related_name="executor",
        on_delete=models.PROTECT,
        verbose_name=_("Executor"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(LabelModel, blank=True, verbose_name=_("Labels"))

    def __str__(self):
        return self.name
