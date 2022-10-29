from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.contrib.messages import get_messages
from django.utils.translation import gettext
from django import test

from task_manager.statuses.models import StatusModel
from task_manager.tests import PASSWORD


@test.modify_settings(
    MIDDLEWARE={
        "remove": [
            "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
        ]
    }
)
class TestView(TestCase):
    fixtures = [
        "task_manager/fixtures/labels.json",
        "task_manager/fixtures/statuses.json",
        "task_manager/fixtures/users.json",
        "task_manager/fixtures/tasks.json",
    ]

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.status_in_use = StatusModel.objects.get(pk=1)
        self.status_unused = StatusModel.objects.get(pk=2)
        self.all_statuses_url = reverse_lazy("all_statuses")

    def test_create_status_GET(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(reverse_lazy("create_status"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/CreationPage.html")

    def test_create_status_POST(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.post(reverse_lazy("create_status"), {"name": "status"})
        message = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(message), 1)
        self.assertEquals(str(message[0]), gettext("Status created"))
        self.assertRedirects(response, self.all_statuses_url)
        self.assertTrue(StatusModel.objects.get(name="status"))

    def test_update_status_GET(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(
            reverse_lazy("update_status", kwargs={"pk": self.status_in_use.pk})
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/UpdatePage.html")

    def test_update_status_POST(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.post(
            reverse_lazy("update_status", kwargs={"pk": self.status_in_use.pk}),
            {"name": "new_test_name"},
        )
        message = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(message), 1)
        self.assertEquals(str(message[0]), gettext("Status updated"))
        self.assertRedirects(response, self.all_statuses_url)
        self.assertTrue(StatusModel.objects.get(name="new_test_name"))

    def test_delete_status_GET(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(
            reverse_lazy("delete_status", kwargs={"pk": self.status_unused.pk})
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/DeletePage.html")

    def test_delete_status_POST_unused(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.post(
            reverse_lazy("delete_status", kwargs={"pk": self.status_unused.pk})
        )
        message = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(message), 1)
        self.assertEquals(str(message[0]), gettext("Status deleted"))
        self.assertRedirects(response, self.all_statuses_url)
        self.assertFalse(StatusModel.objects.filter(pk=self.status_unused.pk).exists())

    def test_delete_status_POST_in_use(self):
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.post(
            reverse_lazy("delete_status", kwargs={"pk": self.status_in_use.pk})
        )
        message = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(message), 1)
        self.assertEquals(
            str(message[0]), gettext("Can't delete status because it's in use")
        )
        self.assertRedirects(response, self.all_statuses_url)
