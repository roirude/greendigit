from typing import Any
from django.contrib import admin

from products.models import Product, Category, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    exclude = ('slug',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sub_category', 'quantity', 'price', 'farmer', 'update_at']
    exclude = ('slug','farmer')
    
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if not obj.pk:
            obj.farmer = request.user
        return super().save_model(request, obj, form, change)
