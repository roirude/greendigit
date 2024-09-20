from django.urls import path

from comparison import views


urlpatterns = [
    path('products/', views.ProductComparisonListView.as_view(), name='product_comparison_list'),
    path('add-to-comparison/<slug:slug>/', views.AddToComparisonView.as_view(), name='add_to_comparison'),
]
