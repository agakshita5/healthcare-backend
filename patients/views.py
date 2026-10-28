from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Patient
from .serializers import PatientSerializer

# login required on all endpoints (default permission in settings).
# users only see and manage the patients they created.


# GET, POST /api/patients/
@api_view(["GET", "POST"])
def patient_list(request):
    if request.method == "GET":
        patients = Patient.objects.filter(created_by=request.user)
        return Response(PatientSerializer(patients, many=True).data)

    serializer = PatientSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(created_by=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# GET, PUT, PATCH, DELETE /api/patients/<id>/
@api_view(["GET", "PUT", "PATCH", "DELETE"])
def patient_detail(request, pk):
    # another user's patient returns 404
    patient = get_object_or_404(Patient, pk=pk, created_by=request.user)

    if request.method == "GET":
        return Response(PatientSerializer(patient).data)

    if request.method in ("PUT", "PATCH"):
        serializer = PatientSerializer(
            patient, data=request.data, partial=(request.method == "PATCH")
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    patient.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
