from django.contrib import admin
from django.contrib import admin
from .models import BankProfile, UzcardProfile

class BankProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bank', 'position')
    search_fields = ('user__first_name', 'bank', 'position')
    list_filter = ('bank',)
    ordering = ('user',)

class UzcardProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'position')
    search_fields = ('user__first_name', 'position')
    ordering = ('user',)

# Register the models with the admin site
admin.site.register(BankProfile, BankProfileAdmin)
admin.site.register(UzcardProfile, UzcardProfileAdmin)

