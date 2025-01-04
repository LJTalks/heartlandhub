from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import BusinessSubmissionForm, BusinessUpdateForm
from .models import BusinessUpdate, Business
import os
from django.db.models import Q  # allows for complex queries
from .utils import obfuscate_email, obfuscate_phone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from cloudinary import CloudinaryResource
from django.utils.html import strip_tags


# Main business detail view
def business_detail(request, slug):
    if request.user.is_authenticated:
        # Include drafts in development
        # if os.path.exists('env.py'):
        #     queryset = Business.objects.filter(Q(status=1) | Q(status=0))
        # else:
        queryset = Business.objects.filter(
            Q(status=1) |
            Q(added_by=request.user) |
            Q(business_owner=request.user)
        )
    else:
        # Only show approved businesses for unauthenticated users
        queryset = Business.objects.filter(status=1)

    business = get_object_or_404(queryset, slug=slug)

    obfuscated_email = obfuscate_email(business.contact_email)
    obfuscated_phone = obfuscate_phone(business.contact_phone)

    return render(
        request, 'business/business_detail.html',
        {
            'business': business,
            'obfuscated_email': obfuscated_email,
            'obfuscated_phone': obfuscated_phone
        }
    )


# Add a new business
@login_required
def submit_business(request):
    if request.method == 'POST':
        form = BusinessSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.status = 0
            business.added_by = request.user
            business.save()
            # Thank you page after submission
            return redirect(reverse('business:submission_success'))
    else:
        form = BusinessSubmissionForm()
    return render(request, 'business/submit_business.html', {'form': form})


def submission_success(request):
    return render(request, "business/submission_success.html", {
        "message": "Thank you for your submission!",
        "link": "/",
        "link_text": "Back to Home"
    })


# Edit request for the business listing
@login_required
def update_business(request, slug):
    business = get_object_or_404(Business, slug=slug)

    # Restrict updates for claimed businesses to the business owner
    if business.is_claimed and business.business_owner != request.user:
        messages.error(
            request, "Only the verified owner can update this business."
        )
        return redirect('business:directory')

    if request.method == 'POST':
        form = BusinessUpdateForm(
            request.POST, request.FILES, instance=business)
        if form.is_valid():
            # Extract and serialize cleaned data for JSON compatibility
            update_data = {
                key: (value.url if isinstance(
                    value, CloudinaryResource) else value)
                for key, value in form.cleaned_data.items()
            }

            # Create a BusinessUpdate record for tracking the change
            BusinessUpdate.objects.create(
                business=business,
                updated_by=request.user,
                updated_data=update_data,
                is_reviewed=False,  # Flag the update for review
            )

            # Save the updated business instance
            form.save()

            # Provide feedback and redirect to the business detail page
            messages.success(
                request, "Your updates have been submitted for review.")
            return redirect('business:business_detail', slug=business.slug)
    else:
        # Pre-fill the form with the current business data
        form = BusinessUpdateForm(instance=business)

    # Sanitize current description before rendering
    current_description = strip_tags(business.business_description)

    return render(request, 'business/update_business.html', {
        'form': form,
        'business': business,
        # Pass sanitized description
        'current_description': current_description,
    })


# Show the user which listings they can edit
@login_required
def edit_listings(request):
    # Get businesses the user can edit
    businesses = Business.objects.filter(
        Q(added_by=request.user) | Q(business_owner=request.user)
    )

    return render(request, 'business/directory.html', {  # removed business/
        'businesses': businesses,
        'edit_mode': True  # Flag to indicate we're in "edit mode"
    })


# Business results page
def directory(request):
    # Get all approved businesses ordered by oldest first
    businesses = Business.objects.filter(
        status=1).order_by('date_added')
    paginator = Paginator(businesses, 6)  # Show 6 businesses per page
    page_number = request.GET.get('page')
    # TODO seems like a dupe, check what happens when we have more than 6 listings
    page_obj = paginator.get_page(page_number)

    return render(
        request, 'business/directory.html', {
            'businesses': businesses,
            'paginator': paginator
        }
    )
