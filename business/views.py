from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import BusinessSubmissionForm
from .models import Business
import os
from django.db.models import Q  # allows for complex queries


# Main business detail view
def business_detail(request, slug):
    # Include drafts in development
    # if os.path.exists('env.py'):
    #     queryset = Business.objects.filter(Q(status=1) | Q(status=0))
    # else:
    queryset = Business.objects.filter(status=1)
    business = get_object_or_404(queryset, slug=slug)

    return render(
        request, 'business/business_detail.html', {'business': business})


# For initial business submission form, to be automated later
def submit_business(request):
    if request.method == 'POST':
        form = BusinessSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.is_approved = False
            business.save()
            return redirect('thank_you')  # Replace with your thank you page
    else:
        form = BusinessSubmissionForm()
    return render(request, 'submit_business.html', {'form': form})


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
