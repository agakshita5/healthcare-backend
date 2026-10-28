from rest_framework.test import APITestCase

from users.models import User
from .models import Patient


class PatientApiTests(APITestCase):
    def setUp(self):
        self.me = User.objects.create_user(email="me@x.com", password="Str0ngPass!9", name="me")
        self.other = User.objects.create_user(email="other@x.com", password="Str0ngPass!9", name="other")
        self.client.force_authenticate(self.me)

    def make_patient(self, owner, name="ravi"):
        return Patient.objects.create(name=name, age=40, gender="male", created_by=owner)

    def test_requires_login(self):
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get("/api/patients/").status_code, 401)

    def test_create_sets_owner_from_token(self):
        res = self.client.post("/api/patients/", {
            "name": "ravi", "age": 40, "gender": "male", "created_by": self.other.id,
        }, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["created_by"], self.me.id)

    def test_invalid_input_is_rejected(self):
        res = self.client.post("/api/patients/", {"name": "ravi", "age": 200, "gender": "x"}, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertIn("age", res.data)
        self.assertIn("gender", res.data)

    def test_list_shows_only_my_patients(self):
        self.make_patient(self.me, "mine")
        self.make_patient(self.other, "theirs")
        res = self.client.get("/api/patients/")
        self.assertEqual([p["name"] for p in res.data], ["mine"])

    def test_other_users_patient_is_404(self):
        theirs = self.make_patient(self.other)
        self.assertEqual(self.client.get(f"/api/patients/{theirs.id}/").status_code, 404)
        self.assertEqual(self.client.delete(f"/api/patients/{theirs.id}/").status_code, 404)

    def test_update_then_delete(self):
        mine = self.make_patient(self.me)
        res = self.client.put(f"/api/patients/{mine.id}/", {
            "name": "ravi kumar", "age": 41, "gender": "male",
        }, format="json")
        self.assertEqual(res.data["name"], "ravi kumar")
        self.assertEqual(self.client.delete(f"/api/patients/{mine.id}/").status_code, 204)
        self.assertFalse(Patient.objects.filter(id=mine.id).exists())
