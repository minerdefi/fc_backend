from django.contrib import admin
from .models import ContactSubmission

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email_address', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('first_name', 'last_name', 'email_address', 'message')
    ordering = ('-created_at',)
