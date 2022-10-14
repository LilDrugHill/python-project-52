from django.contrib import admin
from task_manager.statuses.models import StatusModel
from task_manager.labels.models import LabelModel
from task_manager.tasks.models import TaskModel


admin.site.register(StatusModel)
admin.site.register(LabelModel)
admin.site.register(TaskModel)
