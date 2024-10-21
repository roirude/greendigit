from django.forms import ModelForm

from products import models


class ProductForm(ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'
        exclude = ['slug', 'is_stock', 'is_delete', 'farmer', 'created_at', 'update_at']


class ProductReviewForm(ModelForm):
    class Meta:
        model = models.Review
        fields = ['message',]