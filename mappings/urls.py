from django.urls import path

from . import views

urlpatterns = [
    path("mappings/", views.mapping_list),
    path("mappings/<int:pk>/", views.mapping_detail),   # patient id for GET, mapping id for DELETE
]
