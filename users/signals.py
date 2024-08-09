from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(user_signed_up)
def set_user_type_on_signup(request, user, **kwargs):
    user_type = request.session.get('user_type')
    group = None
    if user_type == 'farmer':
        user.is_farmer = True
        user.is_consumer = False
        group = Group.objects.get_or_create(name='Farmers')

    elif user_type == 'consumer':
        user.is_consumer = True
        user.is_farmer = False
        group = Group.objects.get_or_create(name='Consumers')
        
    user.groups.add(group)
    user.save()
    
    if 'user_type' in request.session:
        del request.session['user_type']
        
        
@receiver(social_account_added)
def set_user_type_on_signup_for_social_account(request, sociallogin, **kwargs):
    user = sociallogin.user
    
    if not user.is_farmer and not user.is_consumer:
        return
    
    if user.is_farmer:
        group = Group.objects.get(name='Farmers')
        user.groups.add(group)
    elif user.is_consumer:
        group = Group.objects.get(name='Consumers')
        user.groups.add(group)
        
    user.save()
               