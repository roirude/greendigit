from datetime import datetime

from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView, ListView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy

from pymesomb.operations import PaymentOperation
from pymesomb.utils import RandomGenerator

from payment.models import Transaction, Refund, Receipt
from products.models import Product
from users.models import CustomUser, Farmer, FarmerAndConsumerLink, Consumer
from payment.forms import TransactionForm


class OrderView(LoginRequiredMixin, CreateView):
    template_name = 'payment/checkout.html'
    form_class = TransactionForm
    
    def form_valid(self, form):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        amount = int(product.price * form.cleaned_data.get('product_quantity'))
        transaction_id = f"transaction_{product.code}_{datetime.now().timestamp()}"
        consumer = Consumer.objects.get(user=self.request.user)
        farmer = Farmer.objects.get(user=product.farmer)
        payment_number = form.cleaned_data.get('payment_number')
        
        form.instance.product = product
        form.instance.consumer = consumer.user
        form.instance.amount = amount
        form.instance.transaction_id = transaction_id
        form.save()
        
        operation = PaymentOperation(settings.MESOMB_APPLICATION_KEY, settings.MESOMB_ACCESS_KEY, settings.MESOMB_SECRET_KEY)
        response = operation.make_collect({
            'amount': amount,
            'service' : 'MTN',
            'payer' : payment_number,
            'date' : datetime.now(),
            'nonce': RandomGenerator.nonce(),
            'trxID' : transaction_id
        })
        
        if response.is_operation_success():
            form.instance.status = 'success'
            form.save()
            
            FarmerAndConsumerLink.objects.create(farmer=farmer, consumer=consumer)
            
            farmer.revenue += amount 
            farmer.save()
            
            transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
            Receipt.objects.create(transaction=transaction)
            
            messages.success(self.request, f"Payment successfully completed")
        else:
            form.instance.status = 'failed'
            form.save()
            
            messages.error(self.request, f"Payment failed: {response.message}")
            
        return super(OrderView, self).form_valid(form)
    
    def get_success_url(self):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        redirect_url = reverse('detail_product', kwargs={'slug':product.slug})
        return redirect_url
    
    def get_context_data(self, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        context["product"] = product
        
        return context
    
    
class ReceiptDetailView(DetailView):
    template_name = 'payment/receipt.html'
    model = Receipt
    context_object_name = 'receipt'
        
        
class ReceiptListView(ListView):
    template_name = 'payment/receipt_list.html'
    model = Receipt
    context_object_name = 'receipts'
    
    def get_queryset(self):
        user = self.request.user
        receipts = Receipt.objects.filter(transaction__consumer=user)
        return receipts
    
        