from rest_framework.test import APITestCase

from users.models import User
from .models import Doctor


class DoctorApiTests(APITestCase):
    def setUp(self):
        self.me = User.objects.create_user(email="me@x.com", password="Str0ngPass!9", name="me")
        self.other = User.objects.create_user(email="other@x.com", password="Str0ngPass!9", name="other")
        self.client.force_authenticate(self.me)

    def test_requires_login(self):
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get("/api/doctors/").status_code, 401)

    def test_list_shows_all_doctors(self):
        Doctor.objects.create(name="a", specialization="cardiology", created_by=self.me)
        Doctor.objects.create(name="b", specialization="neurology", created_by=self.other)
        self.assertEqual(len(self.client.get("/api/doctors/").data), 2)

    def test_create_and_duplicate_email(self):
        body = {"name": "meera", "specialization": "cardiology", "email": "meera@clinic.com"}
        res = self.client.post("/api/doctors/", body, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["created_by"], self.me.id)
        res = self.client.post("/api/doctors/", body, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertIn("email", res.data)

    def test_many_doctors_without_email(self):
        for name in ["a", "b"]:
            res = self.client.post("/api/doctors/", {"name": name, "specialization": "ent", "email": ""}, format="json")
            self.assertEqual(res.status_code, 201)

    def test_update_then_delete(self):
        d = Doctor.objects.create(name="b", specialization="ent", created_by=self.other)
        res = self.client.patch(f"/api/doctors/{d.id}/", {"specialization": "dermatology"}, format="json")
        self.assertEqual(res.data["specialization"], "dermatology")
        self.assertEqual(self.client.delete(f"/api/doctors/{d.id}/").status_code, 204)
        self.assertEqual(self.client.get(f"/api/doctors/{d.id}/").status_code, 404)
