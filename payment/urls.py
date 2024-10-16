from django.urls import path

from payment.views import OrderView, ReceiptListView, ReceiptDetailView, FarmerDeliveryListView


urlpatterns = [
    path('receipt/', ReceiptListView.as_view(), name='receipt_list'),
    path("receipt/<slug:slug>/", ReceiptDetailView.as_view(), name="receipt"),
    path('checkout/<slug:slug>/', OrderView.as_view(), name='checkout_payment'),
    path('fm/<slug:slug>/oders/', FarmerDeliveryListView.as_view(), name='farmer_orders'),
]