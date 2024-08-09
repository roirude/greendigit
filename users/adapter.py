from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from allauth.exceptions import ImmediateHttpResponse

from users.models import CustomUser

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        if request.user.is_authenticated and request.user.is_farmer:
            return reverse_lazy('farmer_dashboard')
        elif request.user.is_authenticated and request.user.is_consumer:
            return reverse_lazy('consumer_dashboard')
        else:
            return super().get_login_redirect_url(request)
        

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        if request.user.is_authenticated and request.user.is_farmer:
            return reverse_lazy('farmer_dashboard')
        elif request.user.is_authenticated and request.user.is_consumer:
            return reverse_lazy('consumer_dashboard')
        else:
            return super().get_connect_redirect_url(request, socialaccount)
        
    # def pre_social_login(self, request, sociallogin):
    #     if sociallogin.is_existing:
    #         return super().pre_social_login(request, sociallogin)
        
    #     email = sociallogin.user.email
        
    #     try:
    #         user = CustomUser.objects.get(email=email)
    #         sociallogin.connect(request, user) 
    #         raise ImmediateHttpResponse(redirect(reverse('index'))) 
    #     except CustomUser.DoesNotExist:
    #         request.session['socialaccount_sociallogin'] = sociallogin.serialize()
    #         raise ImmediateHttpResponse(redirect(reverse('choose_user_type')))
        