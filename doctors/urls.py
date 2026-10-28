from django.urls import path

from . import views

urlpatterns = [
    path("doctors/", views.doctor_list),
    path("doctors/<int:pk>/", views.doctor_detail),
]
