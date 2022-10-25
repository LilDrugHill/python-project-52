from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.contrib.messages import get_messages
from django.utils.translation import gettext
from django import test

from task_manager.labels.models import LabelModel
from task_manager.tasks.models import TaskModel
from task_manager.statuses.models import StatusModel
from task_manager.tests.utils import TestUserMixin, PASSWORD


@test.modify_settings(
    MIDDLEWARE={
        "remove": [
            "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
        ]
    }
)
class TestView(TestCase, TestUserMixin):
    def setUp(self) -> None:
        self.client = Client()
        self.user = self.create_test_user_1()
        self.label = self.create_test_label_1()
        self.all_labels_url = reverse_lazy("all_labels")

    def test_create_label_GET(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(reverse_lazy("create_label"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/CreationPage.html")

    def test_create_label_POST(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.post(reverse_lazy("create_label"), {"name": "label"})
        message = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(message), 1)
        self.assertEquals(str(message[0]), gettext("Label created"))
        self.assertRedirects(response, self.all_labels_url)
        self.assertTrue(LabelModel.objects.get(name="label"))

    def test_update_label_GET(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(
            reverse_lazy("update_label", kwargs={"pk": self.label.pk})
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/UpdatePage.html")

    def test_update_label_POST(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.post(
            reverse_lazy("update_label", kwargs={"pk": self.label.pk}),
            {"name": "new_test_name"},
        )
        message = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(message), 1)
        self.assertEquals(str(message[0]), gettext("Label updated"))
        self.assertRedirects(response, self.all_labels_url)
        self.assertTrue(LabelModel.objects.get(name="new_test_name"))

    def test_delete_label_GET(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(
            reverse_lazy("delete_label", kwargs={"pk": self.label.pk})
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/DeletePage.html")

    def test_delete_label_POST_unused(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.post(
            reverse_lazy("delete_label", kwargs={"pk": self.label.pk})
        )
        message = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(message), 1)
        self.assertEquals(str(message[0]), gettext("Label deleted"))
        self.assertRedirects(response, self.all_labels_url)
        self.assertFalse(LabelModel.objects.filter(pk=self.label.pk).exists())

    def test_delete_label_POST_in_use(self):
        self.client.login(username=self.user.username, password=PASSWORD)

        task = TaskModel.objects.create(
            name="asd",
            description="asd",
            status=self.create_test_status_1(),
            executor=self.user,
            author=self.user,
        )
        task.labels.set([self.label])
        task.save()

        response = self.client.post(
            reverse_lazy("delete_label", kwargs={"pk": self.label.pk})
        )
        message = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(message), 1)
        self.assertEquals(
            str(message[0]), gettext("Can't delete label because it's in use")
        )
        self.assertRedirects(response, self.all_labels_url)
