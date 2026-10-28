from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from doctors.models import Doctor
from doctors.serializers import DoctorSerializer
from patients.models import Patient
from .models import Mapping
from .serializers import MappingSerializer

# users only see and change mappings of their own patients.


# GET, POST /api/mappings/
@api_view(["GET", "POST"])
def mapping_list(request):
    if request.method == "GET":
        mappings = (Mapping.objects
                    .filter(patient__created_by=request.user)
                    .select_related("patient", "doctor"))
        return Response(MappingSerializer(mappings, many=True).data)

    # body: {"patient": <id>, "doctor": <id>}
    serializer = MappingSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# same url, different meaning of <pk> (as defined in the assignment):
#   GET    /api/mappings/<patient_id>/  -> doctors assigned to that patient
#   DELETE /api/mappings/<mapping_id>/  -> remove that mapping
@api_view(["GET", "DELETE"])
def mapping_detail(request, pk):
    if request.method == "GET":
        patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
        doctors = Doctor.objects.filter(mappings__patient=patient)
        return Response(DoctorSerializer(doctors, many=True).data)

    mapping = get_object_or_404(Mapping, pk=pk, patient__created_by=request.user)
    mapping.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
