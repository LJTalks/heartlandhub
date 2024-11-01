# moved from ljtalks.apps.py
# ensure that a UserProfile is automatically created
# whenever a new user registers
from django.apps import AppConfig


class MemberConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'member'


def ready(self):
    import member.signals  # Import signals to make them active
