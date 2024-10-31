from django.db import models
from django.contrib.auth.models import User


# Move this to user_profile app when it exists
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255, blank=True, null=True)
    registration_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()  # Only the first IP
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
