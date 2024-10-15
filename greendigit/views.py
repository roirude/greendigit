from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import OuterRef, Subquery, Count

from users.mixins import GroupRequiredMixin
from products.models import Product, SubCategory
from users.models import CustomUser
 
def index(request):
    if request.user.is_authenticated:
        if request.user.is_farmer:
            return redirect('farmer_dashboard')
        elif request.user.is_consumer:
            return redirect('store')
    else:
        return render(request, 'index.html')


class StoreView(ListView):
    model = Product
    template_name = 'greendigit/store.html'
    paginate_by = 50
    
    def get_queryset(self):
        products = Product.objects.filter(is_delete=False).order_by('-created_at')
        search_query = self.request.GET.get('search')
        if search_query:
            products = Product.objects.filter(is_delete=False, name__icontains=search_query)
            if not products:
                products = Product.objects.filter(is_delete=False).order_by('-created_at')
        return products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        subquery = Product.objects.filter(sub_category=OuterRef('sub_category'), is_delete=False).order_by('id').values('id')[:1]
        context['top_products'] = Product.objects.filter(id__in=Subquery(subquery)).distinct()[:8]
        
        context['sub_categories'] = SubCategory.objects.annotate(product_count=Count('product')).filter(product_count__gt=0)

        return context
    

class FarmerStoreView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'greendigit/farmers.html'
    paginate_by = 60
    
    def get_queryset(self):
        farmers = CustomUser.objects.filter(is_farmer=True)
        search_query = self.request.GET.get('search')
        if search_query:
            farmers = CustomUser.objects.filter(is_farmer=True, first_name__icontains=search_query)
            if not farmers:
                farmers = CustomUser.objects.filter(is_farmer=True)
        return farmers
    