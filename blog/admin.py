from django.contrib import admin

from blog.models import ProcessedEmail


@admin.register(ProcessedEmail)
class ProcessedEmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_verified', 'timestamp']
    ordering = ['-timestamp']
