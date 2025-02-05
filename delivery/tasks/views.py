from django.shortcuts import render, redirect
from .models import Restaurants

# Create your views here.
def cafe_list(request):
    tasks = Restaurants.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            Restaurants.objects.create(title=title)
            return redirect('task_list')
    return render(request, 'tasks/task_list.html', {'tasks': tasks})