# To view general contact submissions in admin
from django.contrib import admin
from .models import ContactSubmission


class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'message', 'submitted_at')
    search_fields = ('user__username', 'email', 'message')
    list_filter = ('submitted_at',)


admin.site.register(ContactSubmission, ContactSubmissionAdmin)
