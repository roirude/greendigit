import uuid

from django.db import models
from django.utils.text import slugify

from users.models import CustomUser as Farmer


class Category(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/category/', null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Product, self).save(*args, **kwargs)


class SubCategory(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='images/subcategory/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Product, self).save(*args, **kwargs)


class Product(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    sub_category = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/products/', null=True, blank=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Product, self).save(*args, **kwargs)