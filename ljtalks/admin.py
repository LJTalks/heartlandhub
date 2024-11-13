# To view general contact submissions in admin
from django.contrib import admin
from .models import ContactSubmission
from django_summernote.admin import SummernoteModelAdmin
from .models import LegalDocument


class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'message', 'submitted_at')
    search_fields = ('user__username', 'email', 'message')
    list_filter = ('submitted_at',)


@admin.register(LegalDocument)
class LegalDocumentAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'last_updated')
    search_fields = ('title', 'seo_tags', 'meta_description')
    list_filter = ('last_updated', 'author')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


admin.site.register(ContactSubmission, ContactSubmissionAdmin)
