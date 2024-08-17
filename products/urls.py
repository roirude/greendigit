from django.urls import path

from products import views

urlpatterns = [
    path('fm/<slug:slug>/products/',views.FarmerProductListView.as_view(), name='farmer_products'),
    path('fm/products/add/', views.ProductCreateView.as_view(), name='add_product'),
]
