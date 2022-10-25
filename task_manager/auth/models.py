from django.contrib.auth.models import User


class UserStr(User):
    def __str__(self):
        return self.get_full_name()

    class Meta:
        proxy = True
