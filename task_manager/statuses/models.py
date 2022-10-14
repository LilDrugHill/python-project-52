from django.db import models


class StatusModel(models.Model):
    name = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
