from django.urls import path
from . import views

urlpatterns = [
    path('', views.restaurant_list, name='restaurant_list'),
    path('restaurant/<int:restaurant_id>/', views.dish_list, name='dish_list'),
    path('', views.home, name='home'),  # Главная страница
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('restaurant/<int:restaurant_id>/', views.dish_list, name='dish_list'),
    path('profile/', views.profile, name='profile'),  # Профиль пользователя
    path('tracking/', views.order_tracking, name='order_tracking'),  # Отслеживание заказов
]