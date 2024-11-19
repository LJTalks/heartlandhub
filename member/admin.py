from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.dateformat import format
from emails.models import EmailListSubscriber
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'source',
    )
    search_fields = (
        'user__username',
        'source',
    )


admin.site.register(UserProfile, UserProfileAdmin)


# Extend UserAdmin to include the related profile info
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'user_email',
        'first_name',
        'last_name',
        'last_login',
        'previous_last_login',
        'date_joined',
        'is_staff',         # Added field for staff status
        'is_superuser',      # Added field for superuser status
        'is_email_subscriber'
    )

    def get_source(self, obj):
        return obj.userprofile.source
    get_source.short_description = 'Source'

    def user_email(self, obj):
        return obj.email
    user_email.short_description = "User Email"

    def previous_last_login(self, obj):
        # Check if last_login is None, and handle it accordingly
        if obj.last_login:
            # Logic for showing the previous login
            return format(obj.last_login, 'd/m/Y H:i')
        else:
            return 'Never logged in'

    previous_last_login.short_description = 'Previous Login'

    # Method to check if user is subscribed to the email list
    def is_email_subscriber(self, obj):
        return EmailListSubscriber.objects.filter(
            user=obj).exists()

    is_email_subscriber.boolean = True
    is_email_subscriber.short_description = "Email List Subscriber"


# Unregister the old UserAdmin
admin.site.unregister(User)
# register the custom UserAdmin
admin.site.register(User, CustomUserAdmin)
