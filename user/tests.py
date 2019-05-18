from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

REGISTER_URL = reverse("user:register")
LOGIN_URL = reverse("user:login")
LOGOUT_URL = reverse("user:logout")


class UserTestCase(TestCase):

    def test_register_view(self):

        res = self.client.get(REGISTER_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "user/register.html")

    def test_register_page_redirects_and_user_created(self):

        payload = {
            "username": "test",
            "password1": "django123",
            "password2": "django123",
        }

        res = self.client.post(REGISTER_URL, payload)
        user = User.objects.get(username=payload["username"])

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, LOGIN_URL)
        self.assertTrue(user.check_password(payload["password1"]))

    def test_register_page_on_invalid_data(self):

        payload = {
            "username": "test",
            "password1": "something",
            "password2": "nothing",
        }

        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "user/register.html")

    def test_login_page(self):

        res = self.client.get(LOGIN_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "user/login.html")

    def test_login_page_redirects(self):

        payload = {
            "username": "test",
            "password": "django123"
        }
        User.objects.create_user(username=payload["username"], password=payload["password"])

        res = self.client.post(LOGIN_URL, payload)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("core:list"))

    def test_logout_redirects_to_login(self):
        user = User.objects.create_user(username="test", password="django123")

        self.client.force_login(user)

        res = self.client.get(LOGOUT_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, LOGIN_URL)
