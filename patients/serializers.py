from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "name", "age", "gender", "phone", "address", "medical_history",
                  "created_by", "created_at", "updated_at"]
        # created_by is set from the token, never from the request body
        read_only_fields = ["created_by", "created_at", "updated_at"]
