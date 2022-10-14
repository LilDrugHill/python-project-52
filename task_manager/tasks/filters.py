import django_filters
from .forms import TaskModel
from django.utils.translation import gettext
from django.forms import CheckboxInput


class TaskFilter(django_filters.FilterSet):
    self_task = django_filters.BooleanFilter(
        method="show_self_task", widget=CheckboxInput, label=gettext("Only own tasks")
    )

    class Meta:
        model = TaskModel
        fields = ("status", "executor", "labels")

    def show_self_task(self, queryset, name, value):
        if value is True:
            return queryset.filter(author_id=self.request.user.pk)
        return queryset
