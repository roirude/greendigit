from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView, TemplateView
from django.http import JsonResponse
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator


from products.models import Product, Category, SubCategory
from users.models import CustomUser
from users.mixins import GroupRequiredMixin
from products.forms import ProductForm
    
    
class FarmerProductListView(GroupRequiredMixin, ListView):
    template_name = 'products/farmer/product_list.html'
    context_object_name = 'products'
    model = Product
    group_required = 'Farmers'
    
    
    def get_queryset(self):
        user = self.request.user
        products = Product.objects.filter(is_delete=False, farmer=user).order_by('-created_at')
        return products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = SubCategory.objects.all()
        for category in categories:
            category.last_products = category.product_set.filter(is_delete=False).order_by('-created_at')[:3]
        context['categories'] = categories
        return context
    

class ProductCreateView(GroupRequiredMixin, CreateView):
    template_name = 'products/product_create.html'
    form_class = ProductForm
    group_required = 'Farmers'
    
    def form_valid(self, form):
        form.instance.farmer = self.request.user
        form.save()
        messages.success(self.request, f"Product '{form.instance.name}' added successfully!")
        return super(ProductCreateView, self).form_valid(form)
    
    def get_success_url(self):
        slug = self.request.user.slug
        redirect_url = reverse('farmer_products', kwargs={'slug':slug})
        return redirect_url


class ProductUpdateView(GroupRequiredMixin, UpdateView):
    template_name = 'products/product_update.html'
    form_class = ProductForm
    model = Product
    group_required = 'Farmers'
    
    def form_valid(self, form):
        messages.success(self.request, f"Product '{form.instance.name}' updated succesfully!")
        return super(ProductUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        slug = self.request.user.slug
        redirect_url = reverse('farmer_products', kwargs={'slug': slug})
        return redirect_url
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product"] = Product.objects.get(slug=self.kwargs['slug'])
        return context
    

class ProductDeleteView(GroupRequiredMixin, RedirectView):
    pattern_name = 'farmer_dashboard'
    group_required = 'Farmers'

    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        product.is_delete = True
        product.save()
        messages.success(self.request, f"Product '{product.name}' deleted succesfully!")
        slug = self.request.user.slug
        redirect_url = reverse(self.pattern_name, kwargs={'slug':slug})
        return redirect_url


# class ProductDetailView(DetailView):
#     template_name = 'product/product_detail.html'
#     context_object_name = 'product'
#     model = Product

#     def get_object(self, queryset=None):
#         return get_object_or_404(Product, slug=self.kwargs['slug'])


# class SubCategoryProductListView(ListView):
#     template_name = 'product/sub_category_product_list.html'
#     context_object_name = 'sub_category_products'
#     model = Product
    
#     def get_queryset(self):
#         sub_category = SubCategory.objects.get(slug=self.kwargs['slug'])
#         product = Product.objects.filter(is_delete=False, sub_category=sub_category).order_by('-created_at')
#         return product
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['sub_category'] = SubCategory.objects.get(slug=self.kwargs['slug'])
#         return context
    
    
# class FarmerProductListView(ListView):
#     template_name = 'product/farmer_product_list.html'
#     context_object_name = 'farmer_product_list'
#     model = Product
#     paginator_class = Paginator
#     paginate_by = 9
    
#     def get_queryset(self):
#         products = super().get_queryset()
#         farmer = User.objects.get(slug=self.kwargs['slug'])
#         products = Product.objects.filter(is_delete=False, farmer=farmer).order_by('-created_at')
#         return products


# class GetSubcategoriesView(View):
#     def get(self, request, *args, **kwargs):
#         if request.is_ajax():
#             category_id = request.GET.get('category_id')
#             if category_id:
#                 try:
#                     subcategories = SubCategory.objects.filter(category_id=category_id)
#                     data = [{'id': subcategory.id, 'name': subcategory.name} for subcategory in subcategories]
#                     return JsonResponse(data, safe=False)
#                 except SubCategory.DoesNotExist:
#                     return JsonResponse({'error': 'Subcategories not found for the given category id.'}, status=404)
#         return JsonResponse({'error': 'Invalid request.'}, status=400)
    
