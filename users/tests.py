from rest_framework.test import APITestCase

from .models import User


class AuthApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="doc@x.com", password="Str0ngPass!9", name="doc")

    def test_register_returns_user_and_tokens(self):
        res = self.client.post("/api/auth/register/", {
            "name": "asha", "email": "asha@x.com", "password": "Str0ngPass!9",
        }, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertNotIn("password", res.data["user"])
        self.assertIn("access", res.data)

    def test_register_rejects_duplicate_email_and_weak_password(self):
        res = self.client.post("/api/auth/register/", {
            "name": "x", "email": "doc@x.com", "password": "123",
        }, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertIn("email", res.data)
        self.assertIn("password", res.data)

    def test_login_success(self):
        res = self.client.post("/api/auth/login/", {"email": "doc@x.com", "password": "Str0ngPass!9"}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertIn("refresh", res.data)

    def test_login_wrong_password(self):
        res = self.client.post("/api/auth/login/", {"email": "doc@x.com", "password": "wrong"}, format="json")
        self.assertEqual(res.status_code, 401)
