from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.utils import timezone
# models.py
from django.db import models

class BankCard(models.Model):
    card_num = models.CharField(max_length=16, unique=True)  # card_num как уникальный идентификатор
    issue_date = models.DateField()
    expiry_date = models.DateField()
    balance = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'bank_cards'
    def __str__(self):
        return f"Card {self.card_num} - Balance: {self.balance}"


class Transaction(models.Model):
    card_num = models.ForeignKey(BankCard, on_delete=models.CASCADE, to_field='card_num', db_column='card_num')
    transaction_time = models.DateTimeField()
    transaction_amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'transactions'

    def __str__(self):
        return f"Transaction of {self.transaction_amount} on {self.transaction_time} for card {self.card_num.card_num}"



    def save(self, *args, **kwargs):
        if self.transaction_time and timezone.is_naive(self.transaction_time):
            self.transaction_time = timezone.make_aware(self.transaction_time, timezone.get_current_timezone())
        super().save(*args, **kwargs)


from django.db import models
from django.contrib.auth.models import User


class PendingEmailRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_num = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    recipient_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Request by {self.user.username} for card {self.card_num}"
