from django.contrib import admin
from django.urls import path, include
# from django.shortcuts import render
from django.views.generic import TemplateView
from . import views
from member.views import CustomLoginView
from business.views import directory


# Function to render the maintenance view (if needed)
# def maintenance_view(request):
#     return render(request, 'maintenance.html')

urlpatterns = [
    # Authentication (allauth)
    path('about_us/', views.about_us_view, name='about_us'),
    path('accounts/', include("allauth.urls")),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    # Admin
    path('admin/', admin.site.urls),
    path("blog/", include("blog.urls"), name="blog-urls"),
    path("cancel/", views.donation_cancel, name="donation_cancel"),
    # General Contact URL (for all)
    path('contact/', views.contact_submit, name='contact'),  # form
    # Updated to point to business app
    path('directory/', include('business.urls')),
    # path('disclaimer/', TemplateView.as_view(
    #     template_name="ljtalks/disclaimer.html"), name='disclaimer'),
    path("donate/", views.donation_page, name="donate"),
    path('emails/', include('emails.urls')),
    path('legal/<slug:slug>/', views.legal_document_view, name='legal_document'),
    path('member/', include('member.urls')),
    # path('privacy/', TemplateView.as_view(
    #     template_name="ljtalks/privacy.html"), name='privacy_policy'),
    # path('projects/', views.projects, name='projects'),
    path("success/", views.donation_success, name="success"),
    # path('terms/', TemplateView.as_view(
    #     template_name="ljtalks/terms.html"), name='terms_conditions'),
    path('summernote/', include('django_summernote.urls')),
    path("", directory, name="home"),
]
