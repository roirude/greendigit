from django import forms
from django.contrib.auth.models import Group
from django.urls import reverse_lazy

from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm


USER_COUNTRY_CHOICES = [
    ('cameroon', 'Cameroon'),
    ('france', 'France'),
    ('canada', 'Canada'),
    ('united_state', 'United State'),
    ('ivory_cost', 'Ivory Cost'),
]


class CustomSignupForm(SignupForm):
    country = forms.ChoiceField(choices=USER_COUNTRY_CHOICES)
    
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        country = self.cleaned_data.get('country')
        user_type = request.session.get('user_type')
        user.country = country
        
        if user_type == 'farmer':
            user.is_farmer = True
            user.is_consumer = False
            group = Group.objects.get(name='Farmers')
        elif user_type == 'consumer':
            user.is_farmer = False
            user.is_consumer = True
            group = Group.objects.get(name='Consumers')
        
        if 'user_type' in request.session:
            del request.session['user_type']
            
        user.groups.add(group)   
        user.save()
        return user
    

# class CustomSocialSignupForm(SocialSignupForm):
    
#     def save(self, request):
#         user = super(CustomSocialSignupForm, self).save(request)
#         user_type = request.session.get('user_type')
        
#         if user_type:
#             if user_type == 'farmer':
#                 user.is_farmer = True
#                 user.is_consumer = False
#                 group = Group.objects.get(name='Farmers')
#             elif user_type == 'consumer':
#                 user.is_farmer = False
#                 user.is_consumer = True
#                 group = Group.objects.get(name='Consumers')
            
#             if 'user_type' in request.session:
#                 del request.session['user_type']
                
#             user.groups.add(group)   
#             user.save()
#         return user
    