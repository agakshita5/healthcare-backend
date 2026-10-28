from rest_framework.test import APITestCase

from doctors.models import Doctor
from patients.models import Patient
from users.models import User
from .models import Mapping


class MappingApiTests(APITestCase):
    def setUp(self):
        self.me = User.objects.create_user(email="me@x.com", password="Str0ngPass!9", name="me")
        self.other = User.objects.create_user(email="other@x.com", password="Str0ngPass!9", name="other")
        self.client.force_authenticate(self.me)
        self.patient = Patient.objects.create(name="ravi", age=40, gender="male", created_by=self.me)
        self.their_patient = Patient.objects.create(name="sam", age=30, gender="male", created_by=self.other)
        self.doctor = Doctor.objects.create(name="meera", specialization="cardiology")

    def test_assign_and_duplicate(self):
        body = {"patient": self.patient.id, "doctor": self.doctor.id}
        res = self.client.post("/api/mappings/", body, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data["doctor_name"], "meera")
        self.assertEqual(self.client.post("/api/mappings/", body, format="json").status_code, 400)

    def test_cannot_assign_other_users_patient(self):
        res = self.client.post("/api/mappings/", {
            "patient": self.their_patient.id, "doctor": self.doctor.id,
        }, format="json")
        self.assertEqual(res.status_code, 400)
        self.assertIn("patient", res.data)

    def test_list_shows_only_my_patients_mappings(self):
        Mapping.objects.create(patient=self.patient, doctor=self.doctor)
        Mapping.objects.create(patient=self.their_patient, doctor=self.doctor)
        res = self.client.get("/api/mappings/")
        self.assertEqual([m["patient_name"] for m in res.data], ["ravi"])

    def test_doctors_of_patient(self):
        Mapping.objects.create(patient=self.patient, doctor=self.doctor)
        res = self.client.get(f"/api/mappings/{self.patient.id}/")
        self.assertEqual([d["name"] for d in res.data], ["meera"])
        self.assertEqual(self.client.get(f"/api/mappings/{self.their_patient.id}/").status_code, 404)

    def test_remove_doctor_from_patient(self):
        m = Mapping.objects.create(patient=self.patient, doctor=self.doctor)
        self.assertEqual(self.client.delete(f"/api/mappings/{m.id}/").status_code, 204)
        self.assertFalse(Mapping.objects.filter(id=m.id).exists())

    def test_deleting_doctor_removes_mappings(self):
        Mapping.objects.create(patient=self.patient, doctor=self.doctor)
        self.client.delete(f"/api/doctors/{self.doctor.id}/")
        self.assertEqual(Mapping.objects.count(), 0)
