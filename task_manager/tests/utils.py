from task_manager.auth.models import User
from task_manager.labels.models import LabelModel
from task_manager.statuses.models import StatusModel


USERNAME_1 = "testuserfirst"
PASSWORD = "Asdfg123456"
USERNAME_2 = "testusersecond"


class TestUserMixin:
    def create_test_user_1(self):
        user = User.objects.create_user(username=USERNAME_1)
        user.set_password(PASSWORD)
        user.save()
        return user

    def create_test_user_2(self):
        user = User.objects.create_user(username=USERNAME_2)
        user.set_password(PASSWORD)
        user.save()
        return user

    def create_test_label_1(self):
        label = LabelModel.objects.create(name="test_label_1")
        label.save()
        return label

    def create_test_label_2(self):
        label = LabelModel.objects.create(name="test_label_2")
        label.save()
        return label

    def create_test_status_1(self):
        status = StatusModel.objects.create(name="test_status_1")
        status.save()
        return status
