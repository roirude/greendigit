import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    Group.objects.get_or_create(name='Farmers')
    Group.objects.get_or_create(name='Consumers')

# Create your models here.
class CustomUser(AbstractUser):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, editable=False)
    avatar = models.ImageField(upload_to="Users/avatars/", blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_farmer = models.BooleanField(default=False)
    is_consumer = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.username

    @property
    def complete_username(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.code)
        return super(CustomUser, self).save(*args, **kwargs)