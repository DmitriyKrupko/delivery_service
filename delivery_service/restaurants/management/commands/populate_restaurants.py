import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from restaurants.models import Restaurant, Category, Dish, RestaurantHighlight
import random

class Command(BaseCommand):
    help = 'Загрузка ресторанов и их меню в базу данных'

    def handle(self, *args, **options):
        restaurants_data = [
            {
                "name": "Лидо",
                "description": "Ресторан белорусской кухни с домашней атмосферой. Специализируется на драниках, колдунах и других национальных блюдах. Есть детское меню.",
                "address": "пр-т Независимости, 49",
                "phone": "+375 17 306-30-36",
                "delivery_radius": 7,
                "cuisine_type": "Белорусская кухня",
                "rating": 4.7,
                "reviews_count": 1250,
                "delivery_time": 40,
                "min_order": 20,
                "logo": "restaurants/logos/lido.png",
                "highlights": ["Национальная кухня", "Детское меню", "Большие порции"],
                "categories": [
                    {
                        "name": "Белорусские блюда",
                        "dishes": [
                            {"name": "Драники", "description": "Картофельные оладьи со сметаной", "price": 12.50, "type": "snack"},
                            {"name": "Колдуны", "description": "Картофельные зразы с мясной начинкой", "price": 15.00, "type": "snack"},
                            {"name": "Мачанка", "description": "Традиционное блюдо с блинами и мясом", "price": 18.00, "type": "snack"},
                        ]
                    },
                    {
                        "name": "Супы",
                        "dishes": [
                            {"name": "Борщ", "description": "Свекольный суп со сметаной", "price": 8.50, "type": "snack"},
                            {"name": "Грибная юшка", "description": "Ароматный суп из лесных грибов", "price": 9.00, "type": "snack"},
                        ]
                    },
                    {
                        "name": "Напитки",
                        "dishes": [
                            {"name": "Квас", "description": "Традиционный хлебный квас 0.5л", "price": 3.50, "type": "drink"},
                            {"name": "Сбитень", "description": "Старинный горячий напиток с медом", "price": 4.00, "type": "drink"},
                        ]
                    }
                ]
            },
            {
                "name": "Раковский Бровар",
                "description": "Пивной ресторан с собственной пивоварней. Попробуйте фирменное темное пиво с копчеными ребрышками. По выходным живая музыка.",
                "address": "ул. Витебская, 10",
                "phone": "+375 29 111-22-33",
                "delivery_radius": 5,
                "cuisine_type": "Пивной ресторан, Европейская кухня",
                "rating": 4.5,
                "reviews_count": 980,
                "delivery_time": 45,
                "min_order": 25,
                "logo": "restaurants/logos/rakovskii-brovar.png",
                "highlights": ["Собственная пивоварня", "Живая музыка", "Терраса"],
                "categories": [
                    {
                        "name": "Пиво",
                        "dishes": [
                            {"name": "Темное", "description": "Фирменное темное пиво 0.5л", "price": 7.00, "type": "drink"},
                            {"name": "Светлое", "description": "Светлое пиво 0.5л", "price": 6.50, "type": "drink"},
                            {"name": "Пшеничное", "description": "Пшеничное нефильтрованное 0.5л", "price": 7.50, "type": "drink"},
                        ]
                    },
                    {
                        "name": "Закуски",
                        "dishes": [
                            {"name": "Ребрышки копченые", "description": "Свиные ребрышки с соусом BBQ", "price": 18.00, "type": "snack"},
                            {"name": "Креветки в чесночном соусе", "description": "Тигровые креветки с чесноком", "price": 22.00, "type": "snack"},
                        ]
                    }
                ]
            },
            {
                "name": "McDonald's",
                "description": "Сеть быстрого питания. Биг Мак с двумя котлетами, детские наборы с игрушками, комбо-обеды до -30%. Круглосуточная доставка.",
                "address": "ул. Притыцкого, 156",
                "phone": "+375 44 700-00-11",
                "delivery_radius": 10,
                "cuisine_type": "Фастфуд, Американская кухня",
                "rating": 4.3,
                "reviews_count": 3200,
                "delivery_time": 30,
                "min_order": 15,
                "logo": "restaurants/logos/McDonald’s.png",
                "highlights": ["Круглосуточная доставка", "Детские меню", "Быстрое обслуживание"],
                "categories": [
                    {
                        "name": "Бургеры",
                        "dishes": [
                            {"name": "Биг Мак", "description": "Легендарный бургер с двумя котлетами", "price": 9.00, "type": "burger"},
                            {"name": "Чизбургер", "description": "Классический бургер с сыром", "price": 5.50, "type": "burger"},
                        ]
                    },
                    {
                        "name": "Картофель",
                        "dishes": [
                            {"name": "Картофель фри", "description": "Хрустящая картошка с солью", "price": 4.50, "type": "snack"},
                            {"name": "Картофель по-деревенски", "description": "Картофель с кожурой и специями", "price": 5.00, "type": "snack"},
                        ]
                    },
                    {
                        "name": "Напитки",
                        "dishes": [
                            {"name": "Кола", "description": "Газированный напиток 0.5л", "price": 3.50, "type": "drink"},
                            {"name": "Айс-кофе", "description": "Холодный кофе со льдом", "price": 4.50, "type": "drink"},
                        ]
                    }
                ]
            }
        ]

        for data in restaurants_data:
            try:
                # 1. Создаем/обновляем ресторан без логотипа
                restaurant, created = Restaurant.objects.get_or_create(
                    name=data['name'],
                    defaults={
                        k: v for k, v in data.items() 
                        if k not in ['logo', 'highlights', 'categories']
                    }
                )

                # 2. Загружаем логотип (если указан и файл существует)
                if created and 'logo' in data:
                    logo_path = os.path.join(settings.MEDIA_ROOT, data['logo'])
                    if os.path.exists(logo_path):
                        with open(logo_path, 'rb') as f:
                            restaurant.logo.save(
                                os.path.basename(data['logo']),
                                File(f),
                                save=True
                            )
                        self.stdout.write(f"Логотип добавлен для {restaurant.name}")
                    else:
                        self.stdout.write(self.style.WARNING(f"Файл лого не найден: {logo_path}"))

                # 3. Добавляем особенности ресторана
                if created and 'highlights' in data:
                    for highlight in data['highlights']:
                        RestaurantHighlight.objects.create(
                            restaurant=restaurant,
                            text=highlight
                        )

                # 4. Добавляем категории и блюда
                if created and 'categories' in data:
                    for cat_data in data['categories']:
                        category = Category.objects.create(
                            name=cat_data['name'],
                            restaurant=restaurant,
                            order=random.randint(1, 10)
                        )
                        
                        for dish_data in cat_data['dishes']:
                            Dish.objects.create(
                                name=dish_data['name'],
                                description=dish_data['description'],
                                price=dish_data['price'],
                                dish_type=dish_data['type'],
                                restaurant=restaurant,
                                category=category,
                                cooking_time=random.randint(5, 25)
                            )
                            
                # 5. Уведомление о результате
                action = "Создан" if created else "Обновлен"
                categories_count = len(data.get('categories', []))
                dishes_count = sum(len(cat['dishes']) for cat in data.get('categories', []))
                
                msg = (f"{action} ресторан: {restaurant.name}. "
                      f"Добавлено: {categories_count} категорий, {dishes_count} блюд")
                self.stdout.write(self.style.SUCCESS(msg))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка для {data.get('name')}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("Загрузка завершена!"))