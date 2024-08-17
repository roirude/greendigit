from django.urls import path

from products import views

urlpatterns = [
    path('fm/products/',views.FarmerProductListView.as_view(), name='farmer_products')
]
