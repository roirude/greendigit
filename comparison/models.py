from django.db import models

from users.models import CustomUser
from products.models import Product


class ProductComparison(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    
