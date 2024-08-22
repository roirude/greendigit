from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.core.exceptions import ImmediateHttpResponse

from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect

from users.models import CustomUser

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        if request.user.is_authenticated and request.user.is_farmer:
            return reverse_lazy('farmer_dashboard')
        elif request.user.is_authenticated and request.user.is_consumer:
            return reverse_lazy('store')
        else:
            return super().get_login_redirect_url(request)
        

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        if request.user.is_authenticated and request.user.is_farmer:
            return reverse('farmer_dashboard')
        elif request.user.is_authenticated and request.user.is_consumer:
            return reverse('store')
        else:
            return super().get_connect_redirect_url(request, socialaccount)
        
        
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return super().pre_social_login(request, sociallogin)
        
        email = sociallogin.user.email
        
        try:
            user = CustomUser.objects.get(email=email)
            sociallogin.connect(request, user) 
            raise ImmediateHttpResponse(redirect(reverse('index'))) 
        except CustomUser.DoesNotExist:
            request.session['socialaccount_sociallogin'] = sociallogin.serialize()
            raise ImmediateHttpResponse(redirect(reverse('choose_user_type')))
    
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user_type = request.session.get('user_type')
        
        if user_type:
            if user_type == 'farmer':
                user.is_farmer = True
                group = Group.objects.get(name='Farmers')
                user.groups.add(group)
            elif user_type == 'consumer':
                user.is_consumer = 'True'
                group = Group.objects.get(name='Consumers')
                user.groups.add(group)
        
        if 'user_type' in request.session:
            del request.session['user_type']
                 
        user.save()
        return user