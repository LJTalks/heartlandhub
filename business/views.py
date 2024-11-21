from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import BusinessSubmissionForm, BusinessUpdateForm
from .models import BusinessUpdate, Business
import os
from django.db.models import Q  # allows for complex queries
from .utils import obfuscate_email, obfuscate_phone
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Main business detail view
def business_detail(request, slug):
    # Include drafts in development
    # if os.path.exists('env.py'):
    #     queryset = Business.objects.filter(Q(status=1) | Q(status=0))
    # else:
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


@login_required
def submit_business(request):
    if request.method == 'POST':
        form = BusinessSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.is_approved = False
            business.added_by = request.user
            business.save()
            # Thank you page after submission
            return redirect('submission_success')
    else:
        form = BusinessSubmissionForm()
    return render(request, 'business/submit_business.html', {'form': form})


def submission_success(request):
    return render(request, "submission_success.html", {
        "message": "Thank you for your submission!",
        "link": "/",
        "link_text": "Back to Home"
    })


@login_required
def update_business(request, slug):
    business = get_object_or_404(Business, slug=slug)
    # Restrict updates for claimed businesses to the business owner
    if business.is_claimed and business.business_owner != request.user:
        messages.error(
            request, "Only the verified owner can update this business.")
        return redirect('directory')

    if request.method == 'POST':
        form = BusinessUpdateForm(
            request.POST, request.FILES, instance=business)
        if form.is_valid():
            update_data = form.cleaned_data
            BusinessUpdate.objects.create(
                business=business,
                updated_by=request.user,
                updated_data=update_data,
                is_reviewed=False,
            )
            return redirect('submission_success')  # Thank you page for updates
    else:
        form = BusinessUpdateForm(instance=business)
    return render(request, 'business/update_business.html', {
        'form': form, 'business': business})


# Business results page
def directory(request):
    # Get all approved businesses
    businesses = Business.objects.filter(
        is_approved=True).order_by('-date_added')
    paginator = Paginator(businesses, 6)  # Show 6 businesses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request, 'business/directory.html', {'businesses': businesses})
