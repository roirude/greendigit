from django.urls import path

from payment.views import OrderView, ReceiptListView, ReceiptDetailView


urlpatterns = [
    path('receipt/', ReceiptListView.as_view(), name='receipt_list'),
    path('checkout/<slug:slug>/', OrderView.as_view(), name='checkout_payment'),
]
