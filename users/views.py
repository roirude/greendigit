from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseBadRequest


class ChooseUserTypeView(TemplateView):
    template_name = 'users/choose_user_type.html'


class SetUserTypeView(TemplateView):
    def post(self, *args, **kwargs):
        user_type = self.request.POST.get('user_type')
        
        if user_type in ['farmer', 'consumer']:
            self.request.session['user_type'] = user_type
            return redirect('account_signup')
        else:
            return HttpResponseBadRequest("User type is not valid.")