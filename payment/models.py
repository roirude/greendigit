from django.db import models

from products.models import Product
from users.models import CustomUser


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('suspend', 'Suspend'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('MTN', 'MTN Mobile Money'),
        ('ORANGE', 'Orange Money'),
    ]
    
    transaction_id = models.CharField(max_length=100, unique=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    consumer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES, default='MTN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"
    
    
class Refund(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
    ]
    
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Refund for {self.transaction.transaction_id} - {self.status}"
    

class Invoice(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE),
    invoice_number = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.transaction}"