from django.forms import ModelForm
from django import forms

from payment.models import Transaction

class TransactionForm(ModelForm):
    payment_number = forms.CharField(max_length=12, required=True)
    
    class Meta:
        model = Transaction
        fields = ('product_quantity', 'payment_number')