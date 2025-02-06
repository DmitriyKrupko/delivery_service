from django.shortcuts import render
from .models import Restaurant

# Create your views here.
def index(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/index.html', {'restaurants': restaurants})