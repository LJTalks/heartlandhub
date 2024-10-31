from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
# from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage, send_mail
from django.core.validators import EmailValidator
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django_ratelimit.decorators import ratelimit
from .forms import ContactForm
from .models import UserProfile
from allauth.account.views import LoginView
import logging
import requests
from datetime import date

# How Many Days of Coding count


def about_me_view(request):
    start_date = date(2024, 6, 24)
    current_date = date.today()
    days_coding = (current_date - start_date).days
    print("Days coding:", days_coding)  # Temporary debug line
    return render(request, 'about_me.html', {'days_coding': days_coding})

# View to showcase previous projects


def projects(request):
    projects = [
        {
            "title": "Love Running",
            "description": "A Fictional Running/Social club advertising regular meets. Responsive HTML & CSS. A Code Institute Tutorial, for a social/running club. Hosted on GitHub Pages.",
            "link": "https://ljtalks.github.io/love-running/",
            "image": "images/projects_love-running.png",
        },
        {
            "title": "Whiskey Store",
            "description": "A Fictional Online Whiskey Subscription site. Responsive HTML, CSS and JavaScript. A Code Institute tutorial. Hosted on Github Pages.",
            "link": "https://ljtalks.github.io/whiskey-store/",
            "image": "images/projects_whiskey-drop.png",
        },
        {
            "title": "Love Rosie; A Resume/CV site",
            "description": "A Fictional Online Resume/CV. Responsive HTML, CSS, JavaScript, Bootstrap 4. A Code Institute tutorial. Hosted on Github Pages.",
            "link": "https://ljtalks.github.io/UCD-Resume/",
            "image": "images/projects_love-rosie.png",
        },
        {
            "title": "Inspire Me Journal; My first JavaScript Project",
            "description": "JavaScript web application. Responsive HTML, CSS, JavaScript. Personal project. Hosted on Github pages.",
            "link": "https://ljtalks.github.io/my-new-journal/",
            "image": "images/inspire_me_journal.png",
        },
        {
            "title": "Codestar Blog; A Full Stack Web App",
            "description": "Full stack web application using Django, PostgreSQL, Python, Responsive HTML, CSS, JavaScript, Bootstrap 4. A Code Institute tutorial. Hosted on Heroku.",
            "link": "https://ljtalks-django-blog-5fbe7cf2584e.herokuapp.com/",
            "image": "images/projects_love-rosie.png",
        },
        {
            "title": "The Fallen; A Simple (free) Landing Page",
            "description": "Simple one page landing page to promote a young author's new book.",
            "link": "https://ltjones.carrd.co/",
            "image": "images/projects_thefallen.png",
        },
    ]
    return render(request, 'projects.html', {"projects": projects})


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
            ip_address = request.META.get(
                'HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
            # Capture the source
            source = request.META.get('HTTP_REFERER', '')
            # Update the UserProfile with source and IP
            profile = UserProfile.objects.get_or_create(user=user)[0]
            profile.source = source
            profile.registration_ip = ip_address
            profile.save()

            return redirect(request.META.get('HTTP_REFERER', 'home'))

    return HttpResponse("Too many requests", status=429)


logger = logging.getLogger(__name__)


# General contact form (for anyone)
def contact_submit(request):
    if request.method == 'POST':
        # Get reCAPTCHA token from the POST data
        recaptcha_response = request.POST.get('g-recaptcha-response')

        # Verify the reCAPTCHA token with Google
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        # Send the request to Google for verification
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        # If reCAPTCHA is not successful, return an error
        if not result['success']:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('contact')

        form = ContactForm(request.POST)

        if form.is_valid():
            # Check the honeypot field
            if form.cleaned_data['honeytrap']:
                # If field is completed it's bot's
                # Redirect without sending any email or showing any message
                return redirect('contact')
            else:
                # Process the valid form submission from a real user
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']

                # Prepare the email content
                subject = f"LJTalks Contact Form from {name}"
                content = (
                    f"New Message from: {name}\nEmail: {email}\n\n{message}\n")
                # Send the email
                email_message = EmailMessage(
                    subject=subject,
                    body=content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.DEFAULT_FROM_EMAIL],
                    reply_to=[email]
                )
                # Set X_Priority to flag the email as important
                email_message.extra_headers = {'X-Priority': '1'}
                email_message.send()

                # Show a success message
                messages.success(request, 'Your message has been sent!')

                # Get the next parameter from form and redirect back
                next_url = request.POST.get('next') or 'home'
                return redirect(next_url)
        else:
            messages.error(request, 'There was an error in the form.')
    else:
        form = ContactForm()  # If GET request, just render the empty form

    # For a GET request, just render the contact form
    return render(request, 'contact.html', {'form': form})


# View to handle the "Tester/Beta Access" Form
# We include is_tester validation but after authentication is checked
# to avoid errors for non logged in users
# renamed from "contact"
@login_required
def beta_contact_view(request):
    is_tester = is_in_group(
        request.user, 'testers')
    return render(request, 'beta_contact.html', {'is_tester': is_tester})


# Apply for beta access form (view)
@login_required
def apply_for_beta_access(request):
    is_tester = is_in_group(request.user, 'testers')

    if request.method == 'POST':
        # Process form submission (email me and store response in db)
        reason = request.POST.get('why')

        # Send an email to notify the admin of the application
        subject = f"{request.user} applied for Beta Access",
        content = (
            f"User {request.user.username} applied for beta access.Reason:\n\n{reason}")

        send_mail(
            subject,
            content,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL]  # Admin email
        )

        # Thank the user and redirect
        messages.success(
            request, 'Thank you for applying for Beta Access. You will be notified when your application is reviewed.')
        return HttpResponseRedirect(reverse('beta_features'))

        # Redirect to beta features page after form submission
        # For now, we'll assume manual approval through the admin panel
        # Redirect after applying
        return HttpResponseRedirect(reverse('beta_features'))

    # Render the beta access form
    return render(request, 'apply_for_beta_access.html', {
        'is_tester': is_tester})


# Helper function to check if the user is in the testers group
def is_in_group(user, group_name):
    # Debugging
    print(f"User: {user}")
    print(f"Groups: {user.groups.all()}")

    # Check if user is in the group
    in_group = user.groups.filter(name=group_name).exists()
    print(f"Is user in group '{group_name}': {in_group}")

    return in_group
    # return user.groups.filter(name=group_name).exists()


# This is the Beta Features View
@login_required
def beta_features_view(request):
    logger.info("Beta Features View Called")

    # Debug Check view is called
    # print("Beta Features View called")
    # Check if user is in the testers group
    is_tester = is_in_group(request.user, 'testers')
    logger.info(f"User {request.user} in in group testers: {is_tester}")
    # Display a list of apps the user has access to
    return render(request, 'beta_features.html', {'is_tester': is_tester})


# Beta Access YouTube Data Checker View
@login_required
@never_cache
def youtube_checker_view(request):
    if not request.user.is_authenticated:
        return redirect('account_login')

    # Check if user is in the testers group
    is_tester = is_in_group(request.user, 'testers')
    if not is_tester:
        # Redirect to safe page if user is not authorised TODO they
        # could get the permission form is they are registered
        # or home page (or back to where they were) if not
        messages.error(request, "You don't have access to this feature.")
        return redirect('home')

    return render(request, 'youtube_checker.html', {'is_tester': is_tester})
