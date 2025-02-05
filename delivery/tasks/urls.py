from django.urls import path
from .views import Restaurants

urlpatterns = [
    path('admin/', name='restarunts_list'),
]
