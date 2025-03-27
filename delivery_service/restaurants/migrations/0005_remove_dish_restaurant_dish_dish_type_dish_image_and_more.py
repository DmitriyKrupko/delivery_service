# Generated by Django 5.1.5 on 2025-03-27 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_order_comments_order_delivery_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='restaurant',
        ),
        migrations.AddField(
            model_name='dish',
            name='dish_type',
            field=models.CharField(choices=[('burger', 'Бургер'), ('snack', 'Закуска'), ('drink', 'Напиток'), ('salad', 'Салат'), ('dessert', 'Десерт')], default='burger', max_length=20),
        ),
        migrations.AddField(
            model_name='dish',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='dishes/'),
        ),
        migrations.AddField(
            model_name='dish',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='dish',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='dish',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название категории')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активна')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='restaurants.restaurant', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['order', 'name'],
                'unique_together': {('name', 'restaurant')},
            },
        ),
        migrations.AddField(
            model_name='dish',
            name='category',
            field=models.ForeignKey(default='не указано', on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='restaurants.category', verbose_name='Категория'),
            preserve_default=False,
        ),
    ]
