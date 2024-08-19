from django.urls import path

from products import views

urlpatterns = [
    path('fm/products/add/', views.ProductCreateView.as_view(), name='add_product'),
    path('fm/<slug:slug>/products/',views.FarmerProductListView.as_view(), name='farmer_products'),
    path('fm/products/update/<slug:slug>', views.ProductUpdateView.as_view(), name='update_product'),
    path('fm/products/delete/<slug:slug>', views.ProductDeleteView.as_view(), name='delete_product'),
]
