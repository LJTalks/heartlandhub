from django import forms
from .models import Business, BusinessUpdate, BusinessCategory
from django.utils.html import strip_tags


class BusinessSubmissionForm(forms.ModelForm):
    new_business_category = forms.CharField(
        required=False,
        label="Add New Business Category if not listed above",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Add a new category'
        })
    )

    class Meta:
        model = Business
        fields = [
            'business_name', 'business_description', 'business_image',
            'alt_text', 'contact_email', 'contact_phone', 'website',
            'business_category', 'new_business_category', 'location',
            'service_area'
        ]

        widgets = {
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.example.com'
            }),
            'business_category': forms.Select(attrs={'class': 'form-control'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'business_description': forms.Textarea(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'service_area': forms.TextInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'website': 'Please enter a full URL, including "http://" or "https://".',
            'service_area': 'Specify the areas this business serves (e.g., towns, cities, or regions).',
        }

    def clean_website(self):
        website = self.cleaned_data.get('website')
        if website and not website.startswith(('http://', 'https://')):
            website = 'http://' + website
        return website

    def clean(self):
        cleaned_data = super().clean()
        new_category = cleaned_data.get('new_business_category')
        business_category = cleaned_data.get('business_category')

        # If the user provided a new category, add it to the database
        if new_category and not business_category:
            category, created = BusinessCategory.objects.get_or_create(
                name=new_category)
            cleaned_data['business_category'] = category

        return cleaned_data


class BusinessUpdateForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = [
            'business_name', 'business_description', 'business_image',
            'alt_text', 'contact_email', 'contact_phone',
            'website', 'location', 'service_area'
        ]

        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            # Fixed syntax error
            'business_description': forms.Textarea(
                attrs={'rows': 5, 'cols': 40, 'class': 'form-control'}
            ),
            'business_image': forms.FileInput(attrs={'class': 'form-control'}),
            'alt_text': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'service_area': forms.TextInput(attrs={'class': 'form-control'}),
        }

        help_texts = {
            'service_area': 'Specify the areas this business serves (e.g., towns, cities, or regions).',
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Explicitly set plain text as initial value for 'business_description'
            if self.instance and self.instance.business_description:
                self.fields['business_description'].initial = strip_tags(
                    self.instance.business_description
                )

    def clean_business_description(self):
        # Ensure user edits are sanitized before saving
        description = self.cleaned_data.get('business_description', '')
        return strip_tags(description)
