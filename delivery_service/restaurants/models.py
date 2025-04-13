from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.forms import ValidationError

class CustomUser(AbstractUser):
    """Расширенная модель пользователя"""
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name="Телефон"
    )
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True, 
        verbose_name="Аватар"
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username}"

class Restaurant(models.Model):
    """Модель ресторана"""
    name = models.CharField(
        max_length=100, 
        verbose_name="Название ресторана"
    )
    description = models.TextField(
        verbose_name="Описание ресторана"
    )
    address = models.CharField(
        max_length=200, 
        verbose_name="Адрес ресторана"
    )
    phone = models.CharField(
        max_length=20, 
        verbose_name="Телефон ресторана"
    )
    delivery_radius = models.PositiveIntegerField(
        default=5,
        verbose_name="Радиус доставки (км)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    cuisine_type = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Тип кухни"
    )
    rating = models.FloatField(
        null=True, 
        blank=True, 
        verbose_name="Рейтинг"
    )
    reviews_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество отзывов"
    )
    delivery_time = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        verbose_name="Время доставки (мин)"
        )
    min_order = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=15, 
        verbose_name="Минимальный заказ"
        )
    logo = models.ImageField(
        upload_to='restaurants/logos/',
        blank=True,
        null=True,
        verbose_name="Логотип"
    )
    delivery_fee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=200,
        verbose_name="Стоимость доставки"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"
        ordering = ['name']

class RestaurantHighlight(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, 
        related_name='highlights',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=100)
    
    def __str__(self):
        return self.text
class Category(models.Model):
    """Категории блюд"""
    name = models.CharField(
        max_length=50,
        verbose_name="Название категории"
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name="Ресторан"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок сортировки"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['order', 'name']
        unique_together = ('name', 'restaurant')

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"


class Dish(models.Model):
    """Модель блюда"""
    DISH_TYPE_CHOICES = [
        ('burger', 'Бургер'),
        ('snack', 'Закуска'),
        ('drink', 'Напиток'),
        ('salad', 'Салат'),
        ('dessert', 'Десерт'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name="Название"
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Цена"
    )
    dish_type = models.CharField(
        max_length=20,
        choices=DISH_TYPE_CHOICES,
        default='burger',
        verbose_name="Тип блюда"
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='dishes',
        verbose_name="Ресторан"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dishes',
        verbose_name="Категория"
    )
    image = models.ImageField(
        upload_to='dishes/',
        null=True,
        blank=True,
        verbose_name="Изображение"
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Доступно"
    )
    cooking_time = models.PositiveIntegerField(
        default=15,
        verbose_name="Время приготовления (мин)"
    )

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['restaurant']),
        ]


class UserAddress(models.Model):
    """Адреса доставки пользователей"""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name="Пользователь"
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Город"
    )
    street = models.CharField(
        max_length=100,
        verbose_name="Улица"
    )
    house = models.CharField(
        max_length=10,
        verbose_name="Дом"
    )
    apartment = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Квартира"
    )
    entrance = models.CharField(
        max_length=5,
        blank=True,
        verbose_name="Подъезд"
    )
    floor = models.CharField(
        max_length=5,
        blank=True,
        verbose_name="Этаж"
    )
    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий"
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name="Основной адрес"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f"{self.city}, {self.street} {self.house} (кв. {self.apartment})"
    
    @property
    def full_address(self):
        return f"{self.city}, {self.street} {self.house}" + \
            f"{', кв. ' + self.apartment if self.apartment else ''}"


class Cart(models.Model):
    """Корзина пользователя"""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"Корзина {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        return self.items.count()


class CartItem(models.Model):
    """Элемент корзины"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Корзина"
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name="Блюдо"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Количество"
    )
    special_requests = models.TextField(
        blank=True,
        verbose_name="Особые пожелания"
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = ('cart', 'dish')

    def __str__(self):
        return f"{self.dish.name} x{self.quantity}"

    @property
    def total_price(self):
        return self.dish.price * self.quantity


class Order(models.Model):
    """Модель заказа"""
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтвержден'),
        ('preparing', 'Готовится'),
        ('ready', 'Готов к выдаче'),
        ('delivering', 'В пути'),
        ('completed', 'Завершен'),
        ('canceled', 'Отменен'),
    ]
    
    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('card', 'Карта онлайн'),
        ('terminal', 'Карта курьеру'),
    ]
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name="Пользователь"
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name="Ресторан"
    )
    delivery_address = models.ForeignKey(
        UserAddress,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name="Адрес доставки"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default='cash',
        verbose_name="Способ оплаты"
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Итоговая сумма"
    )
    delivery_fee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        verbose_name="Стоимость доставки"
    )
    comments = models.TextField(
        blank=True,
        verbose_name="Комментарии"
    )
    estimated_delivery = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Примерное время доставки"
    )
    actual_delivery = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Фактическое время доставки"
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"

    @property
    def full_address(self):
        return str(self.delivery_address)
    
    def total_price(self):
        return sum(item.total_price for item in self.items.all()) + self.delivery_fee
    
    def save(self, *args, **kwargs):
        # Авторасчет общей суммы при сохранении
        if not self.total:
            self.total = self.items.aggregate(total=Sum('price'))['total'] or 0
        super().save(*args, **kwargs)

    def clean(self):
        # Проверка минимального заказа ресторана
        subtotal = self.items.aggregate(total=sum('price'))['total'] or 0
        if subtotal < self.restaurant.min_order:
            raise ValidationError(f"Минимальный заказ для этого ресторана: {self.restaurant.min_order} ₽")


class OrderItem(models.Model):
    """Элемент заказа"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Заказ"
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name="Блюдо"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name="Количество"
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Цена на момент заказа"
    )
    special_requests = models.TextField(
        blank=True,
        verbose_name="Особые пожелания"
    )

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f"{self.dish.name} x{self.quantity} (заказ #{self.order.id})"

    @property
    def total_price(self):
        return self.price * self.quantity