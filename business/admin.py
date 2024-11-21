from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import (Business, BusinessCategory, Location,
                     ServiceArea, BusinessUpdate)


class BusinessAdmin(SummernoteModelAdmin):
    list_display = ('business_name', 'added_by', 'business_owner',
                    'service_area', 'is_approved', 'is_claimed', 'date_added')
    list_filter = ('is_approved', 'is_claimed', 'business_category')
    search_fields = (
        'business_name', 'business_owner__username', 'added_by__username')
    actions = ['approve_businesses', 'mark_as_claimed']
    prepopulated_fields = {'slug': ('business_name',)}
#     # Enable Summernote for the description field
    summernote_fields = ('business_description',)

    fieldsets = (
        (None, {
            'fields': ('business_name', 'slug', 'business_image', 'alt_text',
                       'business_description')
        }),
        ('Service Area', {
            'fields': ('location', 'service_area')
        }),
        ('Contact Info', {
            'fields': ('contact_email', 'contact_phone', 'website')
        }),
        ('Other Information', {
            'fields': ('is_approved', 'status', 'business_category',
                       'added_by', 'is_claimed', 'business_owner')
        }),
    )

    def approve_businesses(self, request, queryset):
        queryset.update(is_approved=True)
    approve_businesses.short_description = "Approve selected businesses"

    def mark_as_claimed(self, request, queryset):
        queryset.update(is_claimed=True)
    mark_as_claimed.short_description = "Mark selected businesses as claimed"


@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


# Business Update Admin
class BusinessUpdateAdmin(admin.ModelAdmin):
    list_display = ('business', 'updated_by', 'is_reviewed', 'date_submitted')
    list_filter = ('is_reviewed',)
    search_fields = ('business__business_name', 'updated_by__username')

    actions = ['approve_updates']

    def approve_updates(self, request, queryset):
        for update in queryset:
            update.apply_update()
        queryset.update(is_reviewed=True)
    approve_updates.short_description = "Approve selected updates"


admin.site.register(Business, BusinessAdmin)
admin.site.register(BusinessCategory)
admin.site.register(Location)
admin.site.register(BusinessUpdate, BusinessUpdateAdmin)
