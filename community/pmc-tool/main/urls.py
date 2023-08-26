from django.urls import path
from .views import render_results, update_data

urlpatterns = [
    path("", render_results, name="render_results"),
    path('update/', update_data, name='update_data'),
]
