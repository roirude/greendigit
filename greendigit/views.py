from django.shortcuts import render, redirect
from django.views.generic import ListView

from users.mixins import GroupRequiredMixin
from products.models import Product
 
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
    paginate_by = 20
    
    def get_queryset(self):
        products = Product.objects.filter(is_delete=False).order_by('-created_at')
        return products
    