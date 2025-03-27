from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Restaurant, Dish, CustomUser, UserAddress

# Register your models here.
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'dish_type', 'price', 'category')
    list_filter = ('dish_type', 'category')
    search_fields = ('name',)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone', 'avatar')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'street', 'house', 'is_primary')
    list_filter = ('city', 'is_primary')
    search_fields = ('user__username', 'street', 'house')