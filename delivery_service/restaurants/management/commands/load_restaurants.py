import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from restaurants.models import Restaurant

class Command(BaseCommand):  # Этот класс должен быть назван именно "Command"
    help = 'Загрузка ресторанов в базу данных'

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
        "logo": "restaurants/logos/lido.png"
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
        "logo": "restaurants/logos/rakovskii-brovar.png"
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
        "logo": "restaurants/logos/McDonald’s.png"
    }
            # ... другие рестораны ...
        ]

        for data in restaurants_data:
            try:
                # 1. Создаем/обновляем ресторан без логотипа
                restaurant, created = Restaurant.objects.get_or_create(
                    name=data['name'],
                    defaults={
                        k: v for k, v in data.items() 
                        if k != 'logo'
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

                # 3. Уведомление о результате
                msg = f"{'Создан' if created else 'Обновлен'} ресторан: {restaurant.name}"
                self.stdout.write(self.style.SUCCESS(msg))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка для {data.get('name')}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("Загрузка завершена!")) 