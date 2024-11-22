from django import forms
from .models import Business, BusinessUpdate


class BusinessSubmissionForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = [
            'business_name', 'business_description', 'business_image',
            'alt_text', 'contact_email', 'contact_phone',
            'website', 'business_category', 'location', 'service_area'
        ]


class BusinessUpdateForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = [
            'business_name', 'business_description', 'business_image',
            'alt_text', 'contact_email', 'contact_phone',
            'website', 'location', 'service_area'
        ]
