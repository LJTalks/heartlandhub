from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import (Business, BusinessCategory, Location,
                     PendingBusinessUpdate, ServiceArea)


class BusinessAdmin(SummernoteModelAdmin):
    list_display = ('business_name', 'business_owner', 'added_by',
                    'service_area', 'is_approved', 'is_claimed', 'date_added')
    list_filter = ('is_approved', 'is_claimed', 'business_category')
    search_fields = (
        'business_name', 'business_owner__username', 'added_by__username')
    actions = ['approve_businesses']
    prepopulated_fields = {'slug': ('business_name',)}
    # Enable Summernote for the description field
    summernote_fields = ('business_description',)
    autocomplete_fields = ['service_area']

    fieldsets = (
        (None, {
            'fields': ('business_name', 'slug', 'business_image', 'alt_text',
                       'business_description')
        }),
        ('Service Area', {
            'fields': ('location', 'custom_service_area',
                       'service_area')
        }),
        ('Contact Info', {
            'fields': ('contact_email', 'contact_phone', 'website')
        }),
        ('Other Information', {
            'fields': ('is_approved', 'status', 'business_category',
                       'custom_business_category', 'added_by', 'is_claimed',
                       'business_owner')
        }),
    )

    def approve_businesses(self, request, queryset):
        queryset.update(is_approved=True)
        approve_businesses.short_description = "Approve selected businesses"


@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


admin.site.register(Business, BusinessAdmin)
admin.site.register(BusinessCategory)
admin.site.register(Location)
admin.site.register(PendingBusinessUpdate)
