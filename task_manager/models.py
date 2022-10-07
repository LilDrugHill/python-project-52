# from django.db import models
# from django.contrib.auth.models import User
#
#
#
# class TimestampedModel(models.Model):
#     """An abstract model with a pair of timestamps."""
#
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         abstract = True
#
#
# class User(TimestampedModel):
#     """A blog user."""
#
#     username = models.EmailField(unique=True, max_length=15)
#     first_name = models.CharField(max_length=15, null=True)
#     last_name = models.CharField(max_length=15, null=True)
#
#     password = models.CharField()