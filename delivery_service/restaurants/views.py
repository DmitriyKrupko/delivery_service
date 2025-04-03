from django.shortcuts import redirect, render, get_object_or_404
from .models import Restaurant, Dish, Cart, CartItem, Order, OrderItem, UserAddress
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm, AddressForm, RegisterForm, CartItemForm
from django.contrib import messages

def home(request):
    return render(request, 'restaurants/home.html')  # Убедитесь что этот путь верный!

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/restaurant_list.html', {'restaurants': restaurants})

def dish_list(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    dishes = restaurant.dishes.all()
    return render(request, 'restaurants/dish_list.html', {'restaurant': restaurant, 'dishes': dishes})

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

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

@login_required
def profile(request):
    profile_form = ProfileForm(instance=request.user)
    address_form = AddressForm()
    
    # Используем правильный related_name (addresses вместо user_addresses)
    addresses = request.user.addresses.all()  # Изменено здесь

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

@login_required
def cart_view(request):
    cart = request.user.cart
    items = cart.items.select_related('dish')
    return render(request, 'restaurants/cart.html', {
        'cart': cart,
        'items': items
    })

@login_required
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        dish=dish,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart=request.user.cart)
    
    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart=request.user.cart)
    cart_item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart = request.user.cart
    if request.method == 'POST':
        # Создаем заказ
        order = Order.objects.create(
            user=request.user,
            restaurant=cart.items.first().dish.restaurant,
            total=cart.total_price,
            delivery_address=request.POST.get('delivery_address'),
            comments=request.POST.get('comments')
        )
        
        # Переносим товары из корзины в заказ
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                dish=item.dish,
                quantity=item.quantity,
                price=item.dish.price
            )
        
        # Очищаем корзину
        cart.items.all().delete()
        
        return redirect('order_detail', order_id=order.id)
    
    return render(request, 'restaurants/checkout.html', {
        'cart': cart,
        'addresses': request.user.addresses.all()
    })

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'restaurants/order_detail.html', {'order': order})

def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Проверяем, можно ли отменить заказ (только если статус "новый")
    if order.status == 'new':
        order.status = 'canceled'
        order.save()
        messages.success(request, f"Заказ #{order.id} успешно отменен")
    else:
        messages.error(request, "Невозможно отменить заказ с текущим статусом")
    
    return redirect('order_detail', order_id=order.id)

@login_required
def set_primary_address(request, address_id):
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)
    # Сбросить все primary
    request.user.addresses.update(is_primary=False)
    # Установить выбранный
    address.is_primary = True
    address.save()
    return redirect('profile')

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)
    address.delete()
    return redirect('profile')

