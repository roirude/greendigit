from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect


class GroupRequiredMixin(LoginRequiredMixin):
    group_required = None
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('index')
        if not Group.objects.get(name=self.group_required) in request.user.groups.all():
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)