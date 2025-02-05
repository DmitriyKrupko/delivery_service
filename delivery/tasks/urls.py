from django.urls import path
from .views import task_list

urlpatterns = [
    path('admin/', name='restarunts_list'),
]
