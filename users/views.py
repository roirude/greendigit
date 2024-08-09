from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import Group
from django.urls import reverse
from django.views import View

from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.helpers import complete_social_login

from users.mixins import GroupRequiredMixin


class ChooseUserTypeView(TemplateView):
    template_name = 'users/choose_user_type.html'


class SetUserTypeView(View):
    def post(self, *args, **kwargs):
        user_type = self.request.POST.get('user_type')
        sociallogin_data = self.request.session.pop('socialaccount_sociallogin', None)
        
        if sociallogin_data:
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
                
            complete_social_login(self.request, sociallogin)
            
            if  user_type == 'farmer':
                return redirect(reverse('farmer_dashboard'))
            elif user_type == 'consumer':
                return redirect(reverse('consumer_dashboard'))   
        else: 
            
            if user_type in ['farmer', 'consumer']:
                self.request.session['user_type'] = user_type
                return redirect('account_signup')
            else:
                return HttpResponseBadRequest("User type is not valid.")
        
class ConsumerDashboardView(GroupRequiredMixin, TemplateView):
    template_name = 'users/consumers/dashboard.html'
    group_required = 'Consumers'
    

class FarmerDashboardView(GroupRequiredMixin, TemplateView):
    template_name = 'users/farmers/dashboard.html'
    group_required = 'Farmers'