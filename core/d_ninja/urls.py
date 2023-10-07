from django.urls import path, re_path, include
from core.d_ninja.api import api

urlpatterns = [
    path("", api.urls),
]