from django.forms import ModelForm

from payment.models import Transaction

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ('product_quantity', 'payment_method')