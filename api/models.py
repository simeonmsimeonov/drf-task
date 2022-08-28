from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=16, decimal_places=2, default=False)

    def __str__(self):
        return self.title

class Order(models.Model):
    date = models.DateField()
    products = models.ManyToManyField(Product, related_name='products')