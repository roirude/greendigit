from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.http import HttpRequest
from django.http.response import HttpResponse


class GroupRequiredMixin(LoginRequiredMixin):
    pass
    # group_required = None
    
    # def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    #     if not request.user.is_authenticated:
    #         return self.handle_no_permission()
    #     if not Group.objects.get(name=self.group_required) in request.user.groups.all()
    #         raise PermissionDenied
    #     return super().dispatch(request, *args, **kwargs)