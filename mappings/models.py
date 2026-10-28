from django.db import models

from doctors.models import Doctor
from patients.models import Patient


# links one patient to one doctor
class Mapping(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="mappings")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="mappings")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        # same doctor can't be assigned to the same patient twice
        constraints = [
            models.UniqueConstraint(fields=["patient", "doctor"], name="unique_patient_doctor"),
        ]

    def __str__(self):
        return f"{self.patient} -> {self.doctor}"
