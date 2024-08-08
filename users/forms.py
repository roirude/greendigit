from django import forms

from allauth.account.forms import SignupForm


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
        elif user_type == 'consumer':
            user.is_farmer = False
            user.is_consumer = True
        
        if 'user_type' in request.session:
            del request.session['user_type']
            
        user.save()
        return user