from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Business, BusinessCategory, Location, PendingBusinessUpdate


class BusinessAdmin(SummernoteModelAdmin):
    list_display = ('business_name', 'business_owner', 'added_by',
                    'is_approved', 'is_claimed', 'date_added')
    list_filter = ('is_approved', 'is_claimed', 'business_category')
    search_fields = (
        'business_name', 'business_owner__username', 'added_by__username')
    actions = ['approve_businesses']
    prepopulated_fields = {'slug': ('business_name',)}
    # Enable Summernote for the description field
    summernote_fields = ('description',)

    fieldsets = (
        (None, {
            'fields': (
                'business_name',
                'slug',
                'business_owner',
                'added_by',
                'business_category',
                'location',
                'business_image',
                'alt_text',
                'business_description',  # Include description field
                'is_approved',
                'is_claimed',
            )
        }),
    )

    def approve_businesses(self, request, queryset):
        queryset.update(is_approved=True)
    approve_businesses.short_description = "Approve selected businesses"


admin.site.register(Business, BusinessAdmin)
admin.site.register(BusinessCategory)
admin.site.register(Location)
admin.site.register(PendingBusinessUpdate)
