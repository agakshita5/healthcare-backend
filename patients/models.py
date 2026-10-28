from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models


class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(150)])
    gender = models.CharField(max_length=10, choices=Gender.choices)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    # user who added the patient; only they can see or change it
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patients"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
