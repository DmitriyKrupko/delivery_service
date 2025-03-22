from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название ресторана")
    description = models.TextField(verbose_name="Описание ресторана")
    address = models.CharField(max_length=200, verbose_name="Адрес ресторана")
    phone = models.CharField(max_length=20, verbose_name="Телефон ресторана")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"

class Dish(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название блюда")
    description = models.TextField(verbose_name="Описание блюда")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена блюда")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="dishes", verbose_name="Ресторан")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

class DeliveryAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house = models.CharField(max_length=10, verbose_name="Дом")
    apartment = models.CharField(max_length=10, blank=True, verbose_name="Квартира")
    comment = models.TextField(blank=True, verbose_name="Комментарий")

    def __str__(self):
        return f"{self.city}, {self.street} {self.house}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('preparing', 'Готовится'),
        ('delivering', 'В пути'),
        ('completed', 'Завершен'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    total = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)