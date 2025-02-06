from django.urls import path
from .views import index, restaurant_dishes

urlpatterns = [
    path('', index, name='index'),
]

urlpatterns = [
    path('restaurant/<int:restaurant_id>/dishes/', restaurant_dishes, name='restaurant_dishes'),
]