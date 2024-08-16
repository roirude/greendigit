from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, RedirectView, TemplateView
from django.http import JsonResponse
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator


from products.models import Product, Category, SubCategory
from users.models import User
from users.mixins import FarmerRequiredMixin
from products.forms import ProductForm
    
    
# class ProductListView(ListView):
#     template_name = 'product/product_list.html'
#     context_object_name = 'product_list'
#     model = Product
    
#     def get_queryset(self):
#         products = Product.objects.filter(is_delete=False).order_by('-created_at')
#         return products
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         categories = SubCategory.objects.all()
#         for category in categories:
#             category.last_products = category.product_set.filter(is_delete=False).order_by('-created_at')[:3]
#         context['categories'] = categories
#         return context
    

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


# class ProductDetailView(DetailView):
#     template_name = 'product/product_detail.html'
#     context_object_name = 'product'
#     model = Product

#     def get_object(self, queryset=None):
#         return get_object_or_404(Product, slug=self.kwargs['slug'])


# class ProductCreateView(FarmerRequiredMixin, CreateView):
#     template_name = 'product/product_create.html'
#     context_object_name = 'form'
#     form_class = ProductForm
    
#     def form_valid(self, form):
#         form.instance.farmer = self.request.user
#         form.save()
#         messages.success(self.request, f"Product '{form.instance.name}' added successfully!")
#         return super(ProductCreateView, self).form_valid(form)
    
#     def get_success_url(self):
#         slug = self.request.user.slug
#         redirect_url = reverse('farmer_product_list', kwargs={'slug':slug})
#         return redirect_url
    


# class ProductUpdateView(FarmerRequiredMixin, UpdateView):
#     template_name = 'product/product_update.html'
#     context_object_name = 'form'
#     form_class = ProductForm
#     model = Product
    
#     def form_valid(self, form):
#         messages.success(self.request, f"Product '{form.instance.name}' updated succesfully!")
#         return super(ProductUpdateView, self).form_valid(form)
    
#     def get_success_url(self):
#         slug = self.request.user.slug
#         redirect_url = reverse('farmer_product_list', kwargs={'slug': slug})
#         return redirect_url
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["product"] = Product.objects.get(slug=self.kwargs['slug'])
#         return context
    


# class ProductDeleteView(FarmerRequiredMixin, RedirectView):
#     pattern_name = 'farmer_product_list'

#     def get_redirect_url(self, *args, **kwargs):
#         product = get_object_or_404(Product, slug=self.kwargs['slug'])
#         product.is_delete = True
#         product.save()
#         messages.success(self.request, f"Product '{product.name}' deleted succesfully!")
#         slug = self.request.user.slug
#         redirect_url = reverse(self.pattern_name, kwargs={'slug':slug})
#         return redirect_url


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
    
