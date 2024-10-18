from datetime import datetime

from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView, ListView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy

from pymesomb.operations import PaymentOperation
from pymesomb.utils import RandomGenerator

from twilio.rest import Client

from payment.models import Transaction, Refund, Receipt, Delivery
from payment.forms import TransactionForm

from products.models import Product

from users.models import CustomUser, Farmer, FarmerAndConsumerLink, Consumer
from users.mixins import GroupRequiredMixin



class OrderView(LoginRequiredMixin, CreateView):
    template_name = 'payment/checkout.html'
    form_class = TransactionForm
    
    def form_valid(self, form):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        amount = int(product.price * form.instance.product_quantity)
        transaction_id = f"transaction_{product.code}_{datetime.now().timestamp()}"
        consumer = Consumer.objects.get(user=self.request.user)
        farmer = Farmer.objects.get(user=product.farmer)
        payment_number = form.cleaned_data.get('payment_number')
        payment_method = self.request.POST.get('pay_method')
        
        form.instance.product = product
        form.instance.consumer = consumer.user
        form.instance.amount = amount
        form.instance.transaction_id = transaction_id
        form.instance.payment_number = payment_number
        form.instance.payment_method = payment_method
        form.save()
        
        operation = PaymentOperation(settings.MESOMB_APPLICATION_KEY, settings.MESOMB_ACCESS_KEY, settings.MESOMB_SECRET_KEY)
        response = operation.make_collect({
            'amount': amount,
            'service' : payment_method,
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
            receipt = Receipt.objects.create(transaction=transaction)
            
            Delivery.objects.create(receipt_id=receipt)
            
            account_sid = settings.ACCOUNT_SID
            auth_token = settings.AUTH_TOKEN
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                 from_=settings.SENDER_NUMBER,
                 body=f'New Order: {receipt.receipt_id}\nConsumer: {consumer.user.fullname}\n Product: {product.name}\nQuantity: {form.instance.product_quantity}\nAmout: XAF {amount}\nLog in to your account for more details: http://127.0.0.1:8000',
                to='+237656484013',
             )
            
            messages.success(self.request, f"Payment successfully completed")
        else:
            form.instance.status = 'failed'
            form.save()
            
            messages.error(self.request, f"Payment failed: {response.message}")
            
        return super(OrderView, self).form_valid(form)
    
    def get_success_url(self):
        receipt = Receipt.objects.filter(transaction__consumer=self.request.user).latest('created_at')
        redirect_url = reverse('receipt', kwargs={'slug':receipt.slug})
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receipt = get_object_or_404(Receipt,slug=self.kwargs['slug'])
        delivry = Delivery.objects.get(receipt_id=receipt)
        context['delivery_code'] = delivry.delivry_code
        context["product"] = receipt.transaction.product
        context['transaction'] = receipt.transaction
        return context
        
        
class ReceiptListView(ListView):
    template_name = 'payment/receipt_list.html'
    model = Receipt
    context_object_name = 'receipts'
    
    def get_queryset(self):
        user = self.request.user
        receipts = Receipt.objects.filter(transaction__consumer=user)
        return receipts
    

class FarmerDeliveryListView(GroupRequiredMixin, ListView):
    group_required = 'Farmers'
    template_name = 'payment/farmer/delivery_list.html'
    model = Delivery
    context_object_name = 'deliveries'
    