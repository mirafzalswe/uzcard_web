from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class BankProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bank = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.first_name} - {self.bank}"


class UzcardProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)


    def __str__(self):
        return f"{self.user.first_name} - {self.position}"


