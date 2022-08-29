from django.db import models

# Create your models here.

FILTER_CHOICES = (
    ('price', 'price'),
    ('count', 'count')
)

class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=16, decimal_places=2, default=False)

    def __str__(self):
        return self.title



class Order(models.Model):
    date = models.DateField()
    products = models.ManyToManyField(Product, related_name='products')

    def short_date(self):
        month = self.date.strftime('%b')
        year = self.date.strftime('%Y')
        return f"{year} {month}"