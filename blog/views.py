from django.http import HttpResponse

from blog.tasks import create_processed_emails, verify_processed_emails


def homepage(request):
    # create_processed_emails.delay(5)
    verify_processed_emails.delay()
    return HttpResponse('<h1>This is a dummy page</h1>')
