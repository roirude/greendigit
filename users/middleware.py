from django.shortcuts import redirect
from django.urls import reverse

class UserTypeCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if not request.user.is_farmer and not request.user.is_consumer:
                if request.path != reverse('set_user_type'):
                    return redirect('choose_user_type')
        return self.get_response(request)