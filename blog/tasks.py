from celery import shared_task
from django.utils import timezone

from blog.models import ProcessedEmail


@shared_task
def test_scheduled_task(arg: str) -> str:
    """
    We use this as a test task for celery scheduling
    :param arg:
    :return: str
    """
    print(arg)


@shared_task
def create_processed_emails(number: int) -> str:
    for i in range(number):
        email = f'email{i}@gmail.com'
        print(f'creating {email}')
        ProcessedEmail.objects.create(email=email, timestamp=timezone.now())
    return f'Done processing {number} emails!'


@shared_task
def verify_processed_emails() -> str:
    for email in ProcessedEmail.objects.all():
        email.is_verified = True
        email.save()
    return 'Emails verified successfully!'
