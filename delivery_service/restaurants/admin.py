from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Restaurant, Dish, CustomUser, UserAddress, Order, OrderItem, CustomUser, UserAddress

# Register your models here.
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'dish_type', 'restaurant', 'price', 'is_available')
    list_filter = ('dish_type', 'restaurant', 'is_available')  
    search_fields = ('name', 'restaurant__name')
    list_editable = ('price', 'is_available')

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'avatar')}),
    )
@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'street', 'house', 'is_primary')
    list_filter = ('city', 'is_primary')
    search_fields = ('user__username', 'street', 'house')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'status', 'total_price')
    list_filter = ('status', 'restaurant')
    search_fields = ('user__username', 'restaurant__name')
    pass

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass

class UserAddressInline(admin.TabularInline):
    model = UserAddress
    extra = 0  # Количество пустых форм для добавления адресов
    fields = ('city', 'street', 'house', 'apartment', 'is_primary')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [UserAddressInline]  # Встраиваем адреса в админку пользователя
    list_display = ('username', 'email', 'phone', 'get_addresses')
    
    def get_addresses(self, obj):
        return ", ".join([f"{a.city} {a.street}" for a in obj.addresses.all()])
    get_addresses.short_description = 'Адреса'