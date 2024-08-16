from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from django.urls import reverse, reverse_lazy
from django.views import View

from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.helpers import complete_social_login

from users.mixins import GroupRequiredMixin
from users.models import CustomUser
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
                return redirect('consumer_dashboard')  
 
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
        context["last_products"] = Product.objects.filter(is_delete=False).order_by('-created_at')[:5]
        return context
    
    


def choose_user_type(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        
        # Récupérer le sociallogin de la session
        sociallogin = SocialLogin.deserialize(request.session.pop('socialaccount_sociallogin'))
        user = sociallogin.user
        user.user_type = user_type  # Mettre à jour le type d'utilisateur
        user.save()
        
        # Ajouter l'utilisateur au bon groupe
        if user_type == 'farmer':
            user.is_farmer = True
            user.groups.add(Group.objects.get(name='Farmers'))
        elif user_type == 'consumer':
            user.is_consumer = True
            user.groups.add(Group.objects.get(name='Consumer'))

        # Finaliser l'authentification
        sociallogin.save(request)
        return redirect(reverse('account_login'))  # Redirigez vers la page souhaitée

    return render(request, 'choose_user_social_type.html')