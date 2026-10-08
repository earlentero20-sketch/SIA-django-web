import random

from django.db import models
from django.core.validators import MinValueValidator


def generate_product_code():
    while True:
        code = str(random.randint(10000000, 99999999))
        if not Product.objects.filter(product_code=code).exists():
            return code


class Product(models.Model):

    PRODUCT_STATUS = [
        ('Available', 'Available'),
        ('Out_of_stock', 'Out of Stock')
    ]

    product_id = models.AutoField(primary_key=True)
    product_code = models.CharField(max_length=8, unique=True, default=generate_product_code, editable=False)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    supplier = models.CharField(max_length=100)
    status = models.CharField(max_length=12, choices=PRODUCT_STATUS)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.product_code:
            self.product_code = generate_product_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name