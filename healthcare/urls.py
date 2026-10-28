"""
URL configuration for healthcare project.

https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path

# each app's urls get included here as the app is built
urlpatterns = [
    path('admin/', admin.site.urls),
]
