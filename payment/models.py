from datetime import datetime
import uuid

from django.db import models
from django.utils.text import slugify

from products.models import Product
from users.models import CustomUser
from payment.utils import generate_receipt_id, generate_refund_id


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('suspend', 'Suspend'),
    ]
    
    transaction_id = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, editable=False, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    consumer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=100, default='MTN')
    payment_number = models.CharField(max_length=100, default="237400001019")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.transaction_id)
        return super(Transaction, self).save(*args, **kwargs)
    
    
class Refund(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
    ]
    
    slug = models.SlugField(unique=True, editable=False, null=True, blank=True)
    refund_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Refund for {self.transaction.transaction_id} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.refund_id:
            self.receipt_id = generate_refund_id(Refund)
        
        self.slug = slugify(self.refund_id)
        return super(Refund, self).save(*args, **kwargs)


class Receipt(models.Model):
    slug = models.SlugField(unique=True, editable=False, null=True, blank=True)
    receipt_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Receipt {self.receipt_id} for {self.transaction}"
    
    def save(self, *args, **kwargs):
        if not self.receipt_id:
            self.receipt_id = generate_receipt_id(Receipt)
            
        self.slug = slugify(self.receipt_id)
        super(Receipt, self).save(*args, **kwargs)