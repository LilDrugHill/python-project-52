from django.db import models
from task_manager.statuses.models import StatusModel
from django.contrib.auth.models import User
from task_manager.labels.models import LabelModel


class TaskModel(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    status = models.ForeignKey(StatusModel, on_delete=models.PROTECT)
    author = models.ForeignKey(User, related_name="author", on_delete=models.PROTECT)
    executor = models.ForeignKey(
        User, related_name="executor", on_delete=models.PROTECT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField(LabelModel, blank=True)

    def __str__(self):
        return self.name
