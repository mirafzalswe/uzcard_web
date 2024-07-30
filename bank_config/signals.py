from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from .models import BankProfile
# User = get_user_model()

# @receiver(post_save, sender=User)
# def create_proflie(sender, instance, created, **kwargs):
#     if created:
#         BankProfile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()