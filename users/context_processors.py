from .models import BankProfile,UzcardProfile

def user_is_uzcard_profile(request):
    if request.user.is_authenticated:
        return {'is_uzcard_profile': UzcardProfile.objects.filter(user=request.user).exists()}
    return {'is_uzcard_profile': False}
