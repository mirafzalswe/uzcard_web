from django.urls import path
from .views import card_info, confirm_requests

urlpatterns = [
    path('',card_info, name='index' ),
    path('uzcard/',  confirm_requests, name='uzcard'),
    # path('login/', login_view, name='login'),
]