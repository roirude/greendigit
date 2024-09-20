from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse

from comparison.models import ProductComparison
from products.models import Product


class AddToComparisonView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        comparison, created = ProductComparison.objects.get_or_create(user=self.request.user)
        
        if comparison.products.count() < 2:
            comparison.products.add(product)
            comparison.save()
            messages.success(self.request, f'{product.name} has been added to comparison.')
        else:
            messages.error(self.request, f'Error: You can only compare 2 products at a time.')
            
        return redirect(reverse('detail_product', kwargs={'slug': product.slug}))
    

class ProductComparisonListView(TemplateView):
    template_name = 'comparison/products/comparison_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comparison = ProductComparison.objects.filter(user=self.request.user).first()
        context["comparison_products"] = comparison.products.all() if comparison else []
        return context
    