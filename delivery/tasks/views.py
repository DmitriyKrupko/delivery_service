from django.shortcuts import render, redirect
from .models import Restaurants

# Create your views here.
def cafe_list(request):
    tasks = Restaurants.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            Restaurants.objects.create(title=title)
            return redirect('restarunt_list')
    return render(request, 'restarunts/restarunt_list.html', {'tasks': tasks})