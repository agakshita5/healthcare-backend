from rest_framework import serializers

from .models import Mapping


class MappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.name", read_only=True)

    class Meta:
        model = Mapping
        fields = ["id", "patient", "patient_name", "doctor", "doctor_name", "created_at"]

    def validate_patient(self, patient):
        # only user's own patients can be assigned
        if patient.created_by != self.context["request"].user:
            raise serializers.ValidationError("patient not found")
        return patient
