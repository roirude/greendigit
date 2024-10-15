from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, UpdateView, DetailView
from django.contrib.auth.models import Group
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.helpers import complete_social_login

from users.mixins import GroupRequiredMixin
from users.models import CustomUser, FarmerAndConsumerLink, Farmer, Consumer
from products.models import Product


class ChooseUserTypeView(TemplateView):
    template_name = 'users/choose_user_type.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_type_url'] = reverse_lazy('choose_user_type')
        return context


class SetUserTypeView(View):
    def post(self, *args, **kwargs):
        user_type = self.request.POST.get('user_type')
        user = self.request.user
        
        if 'socialaccount_sociallogin' in self.request.session:
            sociallogin_data = self.request.session.pop('socialaccount_sociallogin')
            sociallogin = SocialLogin.deserialize(sociallogin_data)
            user = sociallogin.user
            
            if user_type == 'farmer':
                user.is_farmer = True
                user.is_consumer = False
                group = Group.objects.get(name='Farmers')
            elif user_type == 'consumer':
                user.is_farmer = False
                user.is_consumer = True
                group = Group.objects.get(name='Consumers')
                
            user.save()  
            user.groups.add(group)
            user.save()  
            
            # complete_social_login(self.request, sociallogin)   
                   
            if  user_type == 'farmer':
                return redirect('farmer_dashboard')
            elif user_type == 'consumer':
                return redirect('store')  
 
        else: 
            
            if user_type in ['farmer', 'consumer']:
                self.request.session['user_type'] = user_type
                return redirect('account_signup')
            else:
                return redirect('choose_user_type')
            
        
class ConsumerDashboardView(GroupRequiredMixin, TemplateView):
    template_name = 'users/consumers/dashboard.html'
    group_required = 'Consumers'


class FarmerDashboardView(GroupRequiredMixin, TemplateView):
    template_name = 'users/farmers/dashboard.html'
    group_required = 'Farmers'
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        farmer = Farmer.objects.get(user=self.request.user)
        context["last_products"] = Product.objects.filter(is_delete=False, farmer=self.request.user).order_by('-created_at')[:5]
        context["product_count"] = Product.objects.filter(is_delete=False, farmer=self.request.user).count()
        context['farmer'] = farmer
        
        context["order_count"] = FarmerAndConsumerLink.objects.filter(farmer=farmer).count() or 0
        context['consumer_of_this_farmer_count'] = Consumer.objects.filter(farmerandconsumerlink__farmer=farmer).distinct().count() or 0

            
        
        return context
    
    
def choose_user_type(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        
        sociallogin = SocialLogin.deserialize(request.session.pop('socialaccount_sociallogin'))
        user = sociallogin.user
        user.user_type = user_type 
        user.save()
        
        if user_type == 'farmer':
            user.is_farmer = True
            user.groups.add(Group.objects.get(name='Farmers'))
        elif user_type == 'consumer':
            user.is_consumer = True
            user.groups.add(Group.objects.get(name='Consumer'))

        sociallogin.save(request)
        return redirect(reverse('account_login'))

    return render(request, 'choose_user_social_type.html')


class UserEditProfileView(UpdateView):
    template_name = 'users/edit_profile.html'
    model = CustomUser
    fields = ['first_name','last_name', 'email', 'country', 'phone', 'address', 'city', 'state', 'date_of_birth', 'description', 'avatar', 'cover']

    def form_valid(self, form):
        messages.success(self.request, f"{self.request.user.email}'s profile updated succesfully!")
        return super(UserEditProfileView, self).form_valid(form)

    def get_success_url(self):
        slug = self.request.user.slug
        redirect_url = reverse('edit_profile', kwargs={'slug': slug})
        return redirect_url
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = CustomUser.objects.get(slug=self.kwargs['slug'])
        context['user']=user
        return context
    

class FarmerDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'users/farmers/profile_detail.html'
    context_object_name = 'farmer'
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        farmer = CustomUser.objects.get(slug=self.kwargs['slug'])
        context["farmer_products"] = Product.objects.filter(is_delete=False, farmer=farmer).order_by('-created_at')[:4]
        return context
    