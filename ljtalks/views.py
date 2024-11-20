from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from blog.models import Post
from .forms import ContactForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
import requests
from ljtalks.models import ContactSubmission
from django.contrib.sites.models import Site
from .models import LegalDocument
import stripe
from django.http import JsonResponse


current_site = Site.objects.get_current()


# Donate View
stripe.api_key = settings.STRIPE_SECRET_KEY


def donation_page(request):
    if request.method == "POST":
        try:
            # Get the donation amount from the form in pounds
            amount = request.POST.get('amount', None)

            if not amount or float(amount) < 0.5:
                return JsonResponse({
                    'error': "The minimum donation amount is 50p. Please increase your amount."
                })

            # Convert the amount to pence
            amount_in_pence = int(float(amount) * 100)

            # Create a Stripe Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                            'name': 'Heartland Hub Donation',
                        },
                        'unit_amount': amount_in_pence,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://yourdomain.com/success/',
                cancel_url='https://yourdomain.com/cancel/',
            )

            # Return the session ID to the frontend
            return JsonResponse({'id': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return render(
        request, "donation.html", {
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY
        }
    )


# About Us View
def about_us_view(request):
    latest_post = Post.objects.filter(status=1).latest(
        'publish_date')

    return render(request, 'about_us.html', {
        'latest_post': latest_post
    })


# General contact form (for anyone)
def contact_submit(request):
    if request.method == 'POST':
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
                email = (
                    request.user.email
                    if request.user.is_authenticated
                    else form.cleaned_data['email'])
                message = form.cleaned_data['message']

                # Save to database
                ContactSubmission.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    name=name,
                    email=email,
                    message=message
                )

                # Prepare and send the email
                subject = f"{current_site.name} Contact Form from {name}"
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
        initial_data = {
            'email': request.user.email} if request.user.is_authenticated else {}
        # If GET request, just render the empty form
        form = ContactForm(initial=initial_data)

    # For a GET request, just render the contact form
    return render(request, 'contact.html', {'form': form})


# Legal docs in admin
def legal_document_view(request, slug):
    document = get_object_or_404(LegalDocument, slug=slug)
    return render(request, 'legal_document.html', {'document': document})


# View to showcase previous projects
def projects(request):
    projects = [
        {
            "title": "Codestar Blog; A Full Stack Web App",
            "description":
                "Full stack web application using Django, PostgreSQL, Python, Responsive HTML, CSS, JavaScript, Bootstrap 4. A Code Institute tutorial. Hosted on Heroku.",
            "link": "https://ljtalks-django-blog-5fbe7cf2584e.herokuapp.com/",
            "image": "images/projects_love-rosie.png",
        },
    ]

    latest_post = Post.objects.filter(status=1).latest('publish_date')
    return render(
        request,
        'projects.html',
        {"projects": projects,
         "latest_post": latest_post
         })
