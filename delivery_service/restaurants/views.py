from django.shortcuts import redirect, render, get_object_or_404
from .models import Restaurant, Dish, Cart, CartItem, Order, OrderItem, UserAddress, Category
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm, AddressForm, RegisterForm, CartItemForm
from django.contrib import messages
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from .forms import CustomAuthForm
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template import Template, Context
from django.views.generic import View
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    return render(request, 'restaurants/home.html')

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

# views.py (дополнения)
@login_required
def profile(request):
    # Получение адресов текущего пользователя
    addresses = request.user.addresses.all().order_by('-is_primary', '-created_at')
    
    if request.method == 'POST':
        # Обработка формы профиля
        if 'profile_submit' in request.POST:
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Профиль успешно обновлен")
                return redirect('profile')
        
        # Обработка формы адреса
        elif 'address_submit' in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = request.user
                
                # Если это первый адрес - сделать основным
                if not request.user.addresses.exists():
                    address.is_primary = True
                
                address.save()
                messages.success(request, "Адрес успешно сохранен")
                return redirect('profile')
                
    # Инициализация форм
    profile_form = ProfileForm(instance=request.user)
    address_form = AddressForm()
    
    # Фильтрация заказов
    active_statuses = ['new', 'confirmed', 'preparing', 'ready', 'delivering']
    active_orders = request.user.orders.filter(status__in=active_statuses)
    past_orders = request.user.orders.exclude(status__in=active_statuses)
    
    context = {
        'profile_form': profile_form,
        'address_form': address_form,
        'addresses': addresses,
        'active_orders': active_orders,
        'past_orders': past_orders
    }
    
    return render(request, 'restaurants/profile.html', context)

@login_required
def set_primary_address(request, address_id):
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)
    request.user.addresses.update(is_primary=False)
    address.is_primary = True
    address.save()
    messages.success(request, "Основной адрес успешно обновлен")
    return redirect('profile')

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)
    address.delete()
    messages.success(request, "Адрес успешно удален")
    return redirect('profile') 


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

@login_required(login_url='login')
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
    
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        dish=dish,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    messages.success(request, f"«{dish.name}» добавлен в корзину!")
    return redirect(request.META.get('HTTP_REFERER', 'cart'))

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
    
    if not cart.items.exists():
        messages.error(request, "Ваша корзина пуста")
        return redirect('cart')
    
    restaurant_ids = set(item.dish.restaurant.id for item in cart.items.all())
    if len(restaurant_ids) > 1:
        messages.error(request, "Все товары в корзине должны быть из одного ресторана")
        return redirect('cart')
    
    if request.method == 'POST':
        try:
            address_id = request.POST.get('delivery_address')
            address = get_object_or_404(UserAddress, id=address_id, user=request.user)
            restaurant = cart.items.first().dish.restaurant
            
            order = Order.objects.create(
                user=request.user,
                restaurant=restaurant,
                delivery_address=address,
                total=cart.total_price,
                delivery_fee=restaurant.delivery_fee,
                comments=request.POST.get('comments', ''),
                status='new'
            )
            
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    dish=item.dish,
                    quantity=item.quantity,
                    price=item.dish.price,
                    special_requests=item.special_requests
                )
            
            cart.items.all().delete()
            
            # Перенаправляем на страницу подтверждения
            return redirect('order_confirmation', order_id=order.id)
            
        except Exception as e:
            messages.error(request, f"Ошибка при оформлении заказа: {str(e)}")
            return redirect('checkout')
    
    return render(request, 'restaurants/checkout.html', {
        'cart': cart,
        'addresses': request.user.addresses.all(),
        'restaurant': cart.items.first().dish.restaurant if cart.items.exists() else None
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


def menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    categories = restaurant.categories.filter(is_active=True).prefetch_related('dishes')
    
    # Проверяем есть ли вообще блюда в ресторане
    has_dishes = any(category.dishes.exists() for category in categories)

    # Собираем все блюда по категориям
    menu_data = []
    for category in categories:
        dishes = category.dishes.filter(is_available=True)
        if dishes.exists():
            menu_data.append({
                'category': category,
                'dishes': dishes
            })
    
    # Проверяем, есть ли у пользователя корзина
    cart_items = []
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = cart.items.values_list('dish_id', flat=True)
    
    return render(request, 'restaurants/menu.html', {
        'restaurant': restaurant,
        'menu_data': menu_data if has_dishes else None,  # Передаем None если нет блюд
        'cart_items': cart_items,
        'has_dishes': has_dishes
    })

@method_decorator(login_required, name='dispatch')
class DishDetailView(DetailView):
    model = Dish
    template_name = 'restaurants/dish_detail.html'
    context_object_name = 'dish'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
            if cart:
                cart_item = cart.items.filter(dish=self.object).first()
                context['in_cart'] = cart_item.quantity if cart_item else 0
        return context
    
@login_required
def cart_count(request):
    cart = request.user.cart
    count = cart.items.count() if hasattr(request.user, 'cart') else 0
    return JsonResponse({'count': count})

def create_order(request):
    if request.method == 'POST':
        form = OrderItem(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('order_confirmation', order_id=order.id)
    
    try:
       
        restaurant = Cart.items.first().dish.restaurant
        
        
        order = Order.objects.create(
            user=request.user,
            restaurant=restaurant,
            delivery_address=request.user.addresses.filter(is_primary=True).first(),
            total=0, 
            delivery_fee=restaurant.delivery_fee 
        )
        
       
        for cart_item in Cart.items.all():
            OrderItem.objects.create(
                order=order,
                dish=cart_item.dish,
                quantity=cart_item.quantity,
                price=cart_item.dish.price,
                special_requests=cart_item.special_requests
            )
        
       
        Cart.items.all().delete()
        messages.success(request, "Заказ успешно оформлен!")
        return redirect('order_detail', order_id=order.id)
    
    except Exception as e:
        messages.error(request, f"Ошибка: {str(e)}")
        return redirect('cart_view')
    
@login_required
def restaurant_orders(request):
    orders = Order.objects.filter(
        restaurant__owner=request.user  
    ).order_by('-created_at')
    return render(request, 'restaurants/orders.html', {'orders': orders})

def repeat_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        for item in order.items.all():
           
            if not item.dish.is_available:
                raise Exception(f"Блюдо '{item.dish.name}' больше недоступно")
                
            CartItem.objects.create(
                cart=cart,
                dish=item.dish,
                quantity=item.quantity,
                special_requests=item.special_requests
            )
            
        messages.success(request, "Заказ добавлен в корзину!")
    except Exception as e:
        messages.error(request, str(e))
    
    return redirect('cart_view')

def cancel_order(request, order_id):
    
    order = get_object_or_404(
        Order, 
        id=order_id, 
        user=request.user 
    )
    
    
    if order.status in ['new', 'confirmed']:
        order.status = 'canceled'
        order.save()
        messages.success(request, f"Заказ #{order.id} отменен")
    else:
        messages.error(request, "Нельзя отменить заказ в текущем статусе")
    
    return redirect('profile')

class CustomLoginView(LoginView):
    form_class = CustomAuthForm
    template_name = 'registration/login.html'
    extra_context = {'form': CustomAuthForm()}
    pass

class OrderConfirmationView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'restaurants/order_confirmation.html'
    context_object_name = 'order'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)