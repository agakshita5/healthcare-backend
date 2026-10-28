from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Doctor
from .serializers import DoctorSerializer

# doctors are shared: any logged-in user can view and manage all doctors.


# GET, POST /api/doctors/
@api_view(["GET", "POST"])
def doctor_list(request):
    if request.method == "GET":
        return Response(DoctorSerializer(Doctor.objects.all(), many=True).data)

    serializer = DoctorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(created_by=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# GET, PUT, PATCH, DELETE /api/doctors/<id>/
@api_view(["GET", "PUT", "PATCH", "DELETE"])
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == "GET":
        return Response(DoctorSerializer(doctor).data)

    if request.method in ("PUT", "PATCH"):
        serializer = DoctorSerializer(
            doctor, data=request.data, partial=(request.method == "PATCH")
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    doctor.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
