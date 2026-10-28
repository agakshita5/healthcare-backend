from django.conf import settings
from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    # optional but unique; empty is stored as NULL so it doesn't clash
    email = models.EmailField(unique=True, null=True, blank=True)
    # doctors are shared; keep the doctor if the user who added them is deleted
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name="doctors_added",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.specialization})"
