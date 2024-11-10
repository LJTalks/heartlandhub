from django.contrib import admin
from .models import Business, BusinessCategory, Location, PendingBusinessUpdate


class BusinessAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'business_owner', 'added_by',
                    'is_approved', 'is_claimed', 'date_added')
    list_filter = ('is_approved', 'is_claimed', 'business_category')
    search_fields = (
        'business_name', 'business_owner__username', 'added_by__username')
    actions = ['approve_businesses']

    def approve_businesses(self, request, queryset):
        queryset.update(is_approved=True)
    approve_businesses.short_description = "Approve selected businesses"


admin.site.register(Business, BusinessAdmin)
admin.site.register(BusinessCategory)
admin.site.register(Location)
admin.site.register(PendingBusinessUpdate)
