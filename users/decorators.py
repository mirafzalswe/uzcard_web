from django.http import HttpResponseForbidden
from .models import UzcardProfile,BankProfile

def user_has_uzcard_profile(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if UzcardProfile.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view_func


def bank_has_bank_profile(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if BankProfile.objects.filter(user=request.user).exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view_func
