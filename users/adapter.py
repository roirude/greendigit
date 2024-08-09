from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse_lazy


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        if request.user.is_authenticated and request.user.is_farmer:
            return reverse_lazy('farmer_dashboard')
        elif request.user.is_authenticated and request.user.is_consumer:
            return reverse_lazy('consumer_dashboard')
        else:
            return super().get_login_redirect_url(request)