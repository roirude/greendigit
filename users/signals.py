from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(user_signed_up)
def set_user_type_on_signup(request, user, **kwargs):
    user_type = request.session.get('user_type')
    if user_type == 'farmer':
        user.is_farmer = True
        user.is_consumer = False
        group = Group.objects.get_or_create(name='Farmers')

    elif user_type == 'consumer':
        user.is_consumer = True
        user.is_farmer = False
        group = Group.objects.get_or_create(name='Consumers')
        
    user.group.add(group)
    user.save()
    
    if 'user_type' in request.session:
        del request.session['user_type']