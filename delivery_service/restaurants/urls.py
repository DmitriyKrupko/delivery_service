from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView
from .views import (
    home, restaurant_list, dish_list, 
    profile, order_tracking, register,
    cart_view, add_to_cart, update_cart_item, 
    remove_from_cart, checkout, order_detail,
    set_primary_address, delete_address, menu,
    DishDetailView, cart_count, create_order, 
    cancel_order, repeat_order, OrderConfirmationView
)

urlpatterns = [
    path('', home, name='home'),
    path('restaurants/', restaurant_list, name='restaurant_list'),
    path('restaurants/<int:restaurant_id>/', dish_list, name='dish_list'),
    path('profile/', profile, name='profile'),
    path('tracking/', order_tracking, name='order_tracking'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:dish_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', update_cart_item, name='update_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),
    path('menu/<int:restaurant_id>/', menu, name='menu'),
    path('dish/<int:pk>/', DishDetailView.as_view(), name='dish_detail'),
    path('cart/count/', cart_count, name='cart_count'),
    path('order/create/', create_order, name='create_order'),
    path('order/cancel/<int:order_id>/', cancel_order, name='cancel_order'),
    path('order/repeat/<int:order_id>/', repeat_order, name='repeat_order'),
    # Один экземпляр путей для адресов:
    path('address/set-primary/<int:address_id>/', set_primary_address, name='set_primary_address'),
    path('address/delete/<int:address_id>/', delete_address, name='delete_address'),
    #Корзина
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:dish_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', update_cart_item, name='update_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/count/', cart_count, name='cart_count'),
    path('order/confirm/<int:order_id>/', OrderConfirmationView.as_view(), name='order_confirmation')
]