from django.shortcuts import redirect, render, get_object_or_404
from .models import Restaurant, Dish
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm, AddressForm, RegisterForm

def home(request):
    return render(request, 'restaurants/home.html')  # Убедитесь что этот путь верный!

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/restaurant_list.html', {'restaurants': restaurants})

def dish_list(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    dishes = restaurant.dishes.all()
    return render(request, 'restaurants/dish_list.html', {'restaurant': restaurant, 'dishes': dishes})

@login_required
def profile(request):
    return render(request, 'restaurants/profile.html')

def order_tracking(request):
    return render(request, 'restaurants/order_tracking.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    profile_form = ProfileForm(instance=request.user)
    address_form = AddressForm()
    addresses = request.user.user_addresses.all()

    if request.method == 'POST':
        if 'profile_submit' in request.POST:
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile')
                
        elif 'address_submit' in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = request.user
                address.save()
                return redirect('profile')

    return render(request, 'restaurants/profile.html', {
        'profile_form': profile_form,
        'address_form': address_form,
        'addresses': addresses
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('profile')  # Перенаправление на профиль
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})