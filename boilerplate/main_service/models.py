from django.core.validators import MinValueValidator
from django.db import models

from .validators import validate_higher_than_zero


class Product(models.Model):
    name = models.CharField(max_length=64)
    base_price = models.IntegerField(validators=[validate_higher_than_zero])
    description = models.CharField(max_length=128)
    weight = models.FloatField(validators=[validate_higher_than_zero])
    category = models.CharField(max_length=32)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Product, self).save(*args, **kwargs)
