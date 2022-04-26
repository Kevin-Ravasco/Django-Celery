from django.db import models


class ProcessedEmail(models.Model):
    email = models.EmailField()
    is_verified = models.BooleanField(default=False)
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.email
