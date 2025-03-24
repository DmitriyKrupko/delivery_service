from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Главная страница должна быть первой
    path('', views.home, name='home'),
    
    # Список ресторанов
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    
    # Блюда конкретного ресторана
    path('restaurants/<int:restaurant_id>/', views.dish_list, name='dish_list'),
    
    # Профиль и отслеживание
    # Маршрут для страницы профиля
    path('profile/', views.profile, name='profile'),
    
    #Отслеживание
    path('tracking/', views.order_tracking, name='order_tracking'),
   
    #Регистрация
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]