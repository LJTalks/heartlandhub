from allauth.account.forms import SignupForm
from django import forms
from ljtalks.models import UserProfile
import logging
# from captcha.fields import ReCaptchaField


# Set up the logger for bot detection
logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    honeytrap = forms.CharField(required=False, widget=forms.HiddenInput)
    # pets_name = forms.CharField(required=False, widget=)
    # <div style="position: absolute; left: -2000px;">
    # <input type="text" name="pets_name"  value="" /></div>

    # recaptcha = ReCaptchaField()  # Add reCAPTCHA


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
