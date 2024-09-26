from django.urls import path

from payment.views import OrderView


urlpatterns = [
    path('checkout/<slug:slug>/', OrderView.as_view(), name='checkout_payment'),
]
