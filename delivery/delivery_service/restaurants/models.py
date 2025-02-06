from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    delivery_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name    