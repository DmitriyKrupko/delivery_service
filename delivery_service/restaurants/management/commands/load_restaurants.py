from django.core.management.base import BaseCommand
from restaurants.models import Restaurant

class Command(BaseCommand):
    help = 'Загрузка ресторанов Минска в базу данных'

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
    }
]

        for data in restaurants_data:
            restaurant, created = Restaurant.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'address': data['address'],
                    'phone': data['phone'],
                    'delivery_radius': data['delivery_radius'],
                    'cuisine_type': data.get('cuisine_type', ''),
                    'rating': data.get('rating', 0),
                    'reviews_count': data.get('reviews_count', 0),
                    'delivery_time': data.get('delivery_time', 45),
                    'min_order': data.get('min_order', 15),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан ресторан: {restaurant.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Ресторан {restaurant.name} уже существует'))

        self.stdout.write(self.style.SUCCESS('Загрузка ресторанов завершена!'))