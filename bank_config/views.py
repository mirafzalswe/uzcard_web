from datetime import datetime
import pandas as pd
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from .models import BankCard, Transaction,PendingEmailRequest
import os
from users.decorators import user_has_uzcard_profile, bank_has_bank_profile
import logging
from uzcard_webka_2.settings import EMAIL_HOST_USER
from django.conf import settings
logger = logging.getLogger(__name__)

from django.core.mail import send_mail
import time


@login_required(login_url='users/login/')
@bank_has_bank_profile
def card_info(request):
    card = None
    transactions = []
    error = None
    success_message = None

    if request.method == 'POST':
        card_num = request.POST.get('card_number')
        issue_date_str = request.POST.get('issue_date')
        expiry_date_str = request.POST.get('expiry_date')
        recipient_email = request.POST.get('sender_email')

        issue_date = parse_date(issue_date_str)
        expiry_date = parse_date(expiry_date_str)

        if not issue_date or not expiry_date:
            error = "Пожалуйста, предоставьте действительные даты."
        else:
            try:
                card = get_object_or_404(BankCard, card_num=card_num)
                # Создать ожидающий запрос на email
                pending_request = PendingEmailRequest.objects.create(
                    user=request.user,
                    card_num=card_num,
                    issue_date=issue_date,
                    expiry_date=expiry_date,
                    recipient_email=recipient_email
                )
                success_message = "Запрос успешно создан и ожидает подтверждения."
            except BankCard.DoesNotExist:
                error = "Карта не найдена или неверные данные."

    return render(request, 'bank_config/oborotka.html', {'card': card, 'transactions': transactions, 'error': error, 'success_message': success_message})

def create_and_send_email_with_attachment(card, transactions, issue_date_str, expiry_date_str, recipient_email, sender_email):
    try:
        # Создание DataFrame
        data = [{
            "Card Number": transaction.card_num.card_num,
            "Transaction Time": transaction.transaction_time,
            "Transaction Amount": transaction.transaction_amount,
            "Balance After": transaction.balance_after
        } for transaction in transactions]
        df = pd.DataFrame(data)
        # Проверка директории для временных файлов
        if not os.path.exists(settings.TEMP_FILES_DIR):
            os.makedirs(settings.TEMP_FILES_DIR)
            logger.info(f"Created temporary files directory: {settings.TEMP_FILES_DIR}")

        filename = f"{card.card_num}-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
        excel_file_path = os.path.join(settings.TEMP_FILES_DIR, filename)

        # Сохранение DataFrame в Excel
        df.to_excel(excel_file_path, index=False)

        logger.info(f"Excel file created at {excel_file_path}")

        # Чтение содержимого файла Excel
        with open(excel_file_path, 'rb') as f:
            file_data = f.read()

        # Отправка email с прикрепленным файлом
        email_subject = "Bank Card Transactions"
        email_body = f"Attached are the transactions for card number {card.card_num} from {issue_date_str} to {expiry_date_str}."

        email_message = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=sender_email,
            to=[recipient_email]
        )

        email_message.attach(filename,  file_data,)
        logger.info(f"Sending email to {recipient_email} from {sender_email} with attachment {excel_file_path}")
        try:
            email_message.send()
            print('jonatilid')
        except:
            print("oxshamadi")

        logger.info(f"Email sent successfully to {recipient_email}")

        # Удаление файла после успешной отправки
        os.remove(excel_file_path)
        logger.info(f"File {excel_file_path} deleted after sending email.")
    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}")
        raise e




@login_required(login_url='users/login/')
@user_has_uzcard_profile
def confirm_requests(request):
    pending_requests = PendingEmailRequest.objects.filter(confirmed=False)

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        pending_request = PendingEmailRequest.objects.get(id=request_id)

        # Получить карту и транзакции
        card = get_object_or_404(BankCard, card_num=pending_request.card_num)
        transactions = Transaction.objects.filter(
            card_num=card,
            transaction_time__range=(pending_request.issue_date, pending_request.expiry_date)
        )

        # Отправить email
        try:
            create_and_send_email_with_attachment(
                card,
                transactions,
                pending_request.issue_date.strftime('%Y-%m-%d'),
                pending_request.expiry_date.strftime('%Y-%m-%d'),
                pending_request.recipient_email,
                settings.EMAIL_HOST_USER
            )
            pending_request.confirmed = True
            pending_request.save()
            logger.info(f"Email confirmed and sent for request {request_id}")
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")

    return render(request, 'uzcard/main.html', {'pending_requests': pending_requests})
