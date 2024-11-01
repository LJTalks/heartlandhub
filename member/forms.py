from allauth.account.forms import SignupForm
from django import forms
from member.models import UserProfile
import logging


# Set up the logger for bot detection
logger = logging.getLogger(__name__)


class CustomSignupForm(SignupForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    def save(self, request):
        if self.cleaned_data['honeypot']:
            logger.warning(
                f"Bot detected during signup! IP: {request.META.get(
                    'REMOTE_ADDR')}")

            raise forms.ValidationError("Bot detected!")

        user = super(CustomSignupForm, self).save(request)

        # Capture the source
        source = request.META.get('HTTP_REFERER', '')

        # Update or create the profile with source
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.source = source
        user_profile.save()

        return user
