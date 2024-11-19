from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import CustomSignupForm
from .models import UserProfile
from django.conf import settings
import logging
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from allauth.account.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django_ratelimit.decorators import ratelimit


# Limit to 5 requests per minute per IP
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def register_user(request):
    # Check if user was rate-limited
    was_limited = getattr(request, 'limits', False)
    if was_limited:
        # Custom response for rate-limited requests
        return HttpResponse(
            "You've made too many requests. Please try again later.",
            status=429
        )

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save()
            # Capture the source and IP address, inc behind proxies
            ip_address = get_client_ip(request)
            logger.info(f"Captured IP: {ip_address}")

            source = request.META.get('HTTP_REFERER', '')

            # Update the UserProfile with source and IP
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.source = source
            profile.save()

            return redirect(request.META.get('HTTP_REFERER', 'home'))

    return HttpResponse("Too many requests", status=429)


# IP tracking botwatch
logger = logging.getLogger(__name__)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()  # Only the first IP
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CustomLoginView(LoginView):
    def form_valid(self, form):
        print("Custom login form_valid triggered")

        login_input = form.cleaned_data.get('login')
        validator = EmailValidator()
        try:
            validator(login_input)
            is_email = True
        except ValidationError:
            is_email = False

        if is_email:
            user_exists = User.objects.filter(email=login_input).exists()
        else:
            user_exists = User.objects.filter(username=login_input).exists()

        if not user_exists:
            messages.error(self.request, "Account not found. Please sign up.")
            return redirect('account_signup')
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Custom login form_invalid triggered")
        # Display error message
        messages.error(
            self.request, "Login failed. Please check your credentials.")
        return super().form_invalid(form)


# Password reset, auto log in
@login_required
def password_reset(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after password change
            # Prevents logout after password change
            update_session_auth_hash(request, user)
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password.html', {'form': form})
