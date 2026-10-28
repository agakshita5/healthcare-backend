from django.urls import path

from . import views

urlpatterns = [
    path("patients/", views.patient_list),
    path("patients/<int:pk>/", views.patient_detail),
]
