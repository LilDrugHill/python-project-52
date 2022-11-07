from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.contrib.messages import get_messages
from django.utils.translation import gettext_lazy as _
from django import test

from task_manager.labels.models import LabelModel
from task_manager.utils import SomeFuncsForTestsMixin


@test.modify_settings(
    MIDDLEWARE={
        "remove": [
            "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
        ]
    }
)
class TestView(SomeFuncsForTestsMixin, TestCase):
    fixtures = [
        "task_manager/fixtures/labels.json",
        "task_manager/fixtures/statuses.json",
        "task_manager/fixtures/users.json",
        "task_manager/fixtures/tasks.json",
    ]

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.label_in_use = LabelModel.objects.get(pk=1)
        self.label_unused = LabelModel.objects.get(pk=2)
        self.all_labels_url = reverse_lazy("all_labels")

    def test_create_label_GET(self):
        self.login_user(self.user)
        response = self.client.get(reverse_lazy("create_label"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/CreationPage.html")

    def test_create_label_POST(self):
        self.login_user(self.user)
        response = self.client.post(reverse_lazy("create_label"), {"name": "label"})
        message = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(message), 1)
        self.assertEquals(str(message[0]), _("Label created"))
        self.assertRedirects(response, self.all_labels_url)
        self.assertTrue(LabelModel.objects.get(name="label"))

    def test_update_label_GET(self):
        self.login_user(self.user)
        response = self.client.get(
            reverse_lazy("update_label", kwargs={"pk": self.label_in_use.pk})
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/UpdatePage.html")

    def test_update_label_POST(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse_lazy("update_label", kwargs={"pk": self.label_in_use.pk}),
            {"name": "new_test_name"},
        )
        message = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(message), 1)
        self.assertEquals(str(message[0]), _("Label updated"))
        self.assertRedirects(response, self.all_labels_url)
        self.assertTrue(LabelModel.objects.get(name="new_test_name"))

    def test_delete_label_GET(self):
        self.login_user(self.user)
        response = self.client.get(
            reverse_lazy("delete_label", kwargs={"pk": self.label_unused.pk})
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/DeletePage.html")

    def test_delete_label_POST_unused(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse_lazy("delete_label", kwargs={"pk": self.label_unused.pk})
        )
        message = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(message), 1)
        self.assertEquals(str(message[0]), _("Label deleted"))
        self.assertRedirects(response, self.all_labels_url)
        self.assertFalse(LabelModel.objects.filter(pk=self.label_unused.pk).exists())

    def test_delete_label_POST_in_use(self):
        self.login_user(self.user)
        response = self.client.post(
            reverse_lazy("delete_label", kwargs={"pk": self.label_in_use.pk})
        )
        message = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(message), 1)
        self.assertEquals(str(message[0]), _("Can't delete label because it's in use"))
        self.assertRedirects(response, self.all_labels_url)
