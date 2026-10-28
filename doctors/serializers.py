from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["id", "name", "specialization", "phone", "email",
                  "created_by", "created_at", "updated_at"]
        read_only_fields = ["created_by", "created_at", "updated_at"]

    def validate_email(self, value):
        return value or None    # store "" as NULL
