from django.contrib import admin
from .models import BankCard, Transaction
# Register your models here.
# admin.site.register(BankProfile)
admin.site.register(BankCard)
admin.site.register(Transaction)