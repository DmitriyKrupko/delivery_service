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