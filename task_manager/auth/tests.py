from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.contrib.messages import get_messages
from django.utils.translation import gettext_lazy as _
from django import test

from task_manager.auth.models import User
from task_manager.utils import SomeFuncsForTestsMixin


@test.modify_settings(
    MIDDLEWARE={
        "remove": [
            "rollbar.contrib.django.middleware.RollbarNotifierMiddleware",
        ]
    }
)
class TestViews(SomeFuncsForTestsMixin, TestCase):
    fixtures = [
        "task_manager/fixtures/labels.json",
        "task_manager/fixtures/statuses.json",
        "task_manager/fixtures/users.json",
        "task_manager/fixtures/tasks.json",
    ]

    def setUp(self):
        self.user_1 = User.objects.get(pk=1)
        self.user_2 = User.objects.get(pk=2)
        self.client = Client()
        self.registration_url = reverse_lazy("register")
        self.betrayer_message = _("You are betrayer")
        self.all_users_url = reverse_lazy("all_users")

    def test_register_user_GET(self):
        response = self.client.get(self.registration_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/SignUpPage.html")

    def test_register_user_POST_success_reg(self):
        response = self.client.post(
            self.registration_url,
            {
                "username": "ddenis",
                "first_name": "den",
                "last_name": "cos",
                "password1": "asdasd11Asd",
                "password2": "asdasd11Asd",
            },
        )

        self.assertEquals(response.status_code, 302)
        self.assertTrue(User.objects.get(username="ddenis"))

    def test_update_user_GET_owner(self):
        self.login_user(self.user_1)
        response = self.client.get(
            reverse_lazy("update_user", kwargs={"pk": self.user_1.pk})
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/UpdatePage.html")

    def test_update_user_GET_betrayer(self):
        self.login_user(self.user_2)
        response = self.client.get(
            reverse_lazy("update_user", kwargs={"pk": self.user_1.pk})
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(messages), 1)
        self.assertEquals(str(messages[0]), self.betrayer_message)
        self.assertRedirects(response, self.all_users_url)

    def test_update_user_POST(self):
        self.login_user(self.user_1)
        response = self.client.post(
            reverse_lazy("update_user", kwargs={"pk": self.user_1.pk}),
            {
                "first_name": "some_f_name",
                "last_name": "some_l_name",
                "username": self.user_1.username,
                "password1": self.password,
                "password2": self.password,
            },
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(messages), 1)
        self.assertEquals(str(messages[0]), _("User changed successfully"))
        self.assertTrue(
            User.objects.get(username=self.user_1.username, first_name="some_f_name")
        )
        self.assertRedirects(response, self.all_users_url)

    def test_delete_user_GET_owner(self):
        self.login_user(self.user_2)
        response = self.client.get(
            reverse_lazy("delete_user", kwargs={"pk": self.user_2.pk})
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/DeletePage.html")

    def test_delete_user_GET_betrayer(self):
        self.login_user(self.user_2)
        response = self.client.get(
            reverse_lazy("delete_user", kwargs={"pk": self.user_1.pk})
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(messages), 1)
        self.assertEquals(str(messages[0]), self.betrayer_message)
        self.assertRedirects(response, self.all_users_url)

    def test_delete_user_POST_free_owner(self):
        self.login_user(self.user_2)
        response = self.client.post(
            reverse_lazy("delete_user", kwargs={"pk": self.user_2.pk})
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(messages), 1)
        self.assertEquals(str(messages[0]), _("User deleted"))
        self.assertRedirects(response, self.all_users_url)
        self.assertFalse(User.objects.filter(pk=self.user_2.pk).exists())

    def test_delete_user_POST_author_task(self):
        self.login_user(self.user_1)
        response = self.client.post(
            reverse_lazy("delete_user", kwargs={"pk": self.user_1.pk})
        )
        message = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(message), 1)
        self.assertEquals(
            str(message[0]), _("Cannot delete user because it's in use")
        )
        self.assertRedirects(response, self.all_users_url)

    def test_delete_user_POST_betrayer(self):
        self.login_user(self.user_2)
        response = self.client.post(
            reverse_lazy("delete_user", kwargs={"pk": self.user_1.pk})
        )
        message = list(get_messages(response.wsgi_request))

        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(message), 1)
        self.assertEquals(str(message[0]), self.betrayer_message)
        self.assertRedirects(response, self.all_users_url)
