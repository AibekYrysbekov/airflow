from django.urls import path
from .views import save_data_to_database

urlpatterns = [
    path('', save_data_to_database, name='save_data'),
]
