from django.shortcuts import render, get_object_or_404
from .models import Restaurant, Dish

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/restaurant_list.html', {'restaurants': restaurants})

def dish_list(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    dishes = restaurant.dishes.all()
    return render(request, 'restaurants/dish_list.html', {'restaurant': restaurant, 'dishes': dishes})

def home(request):
    return render(request, 'restaurants/home.html')

def profile(request):
    return render(request, 'restaurants/profile.html')

def order_tracking(request):
    return render(request, 'restaurants/order_tracking.html')