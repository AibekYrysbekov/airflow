from django.urls import path
from .views import render_results

urlpatterns = [
    path("", render_results, name="save_data"),
]
