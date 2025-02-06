from django.shortcuts import render, get_object_or_404
from .models import Restaurant, Dish

# Create your views here.
def index(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/index.html', {'restaurants': restaurants})

def restaurant_dishes(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    dishes = restaurant.dishes.all()  # Получаем все блюда, связанные с рестораном

    context = {
        'restaurant': restaurant,
        'dishes': dishes,
    }
    return render(request, 'restaurants/restaurant_dishes.html', context)