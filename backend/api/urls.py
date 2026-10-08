from django.urls import path

from .views import create_route

urlpatterns = [
    path("routes/", create_route),
]