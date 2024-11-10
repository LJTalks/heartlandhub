from django import forms
from .models import Business


# Temp/initial business submission form, to be automated later
class BusinessSubmissionForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = [
            'business_name', 'business_description', 'location',
            'service_area', 'contact_email', 'contact_phone',
            'website', 'business_category', 'custom_business_category',
            'business_image'
        ]
        widgets = {
            'business_description': forms.Textarea(attrs={'rows': 4}),
        }


# Not using this yet
class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['business_name',
                  'business_description',
                  'location',
                  'custom_location',
                  'service_area',
                  'contact_email',
                  'contact_phone',
                  'website',
                  'business_category',
                  'custom_business_category'
                  ]

    def clean(self):
        cleaned_data = super().clean()
        location = cleaned_data.get("location")
        custom_location = cleaned_data.get("custom_location")
        category = cleaned_data.get("category")
        custom_category = cleaned_data.get("custom_category")

        # Ensure custom_location is filled if "Other" is chosen for location
        if location == "Other" and not custom_location:
            self.add_error("custom_location", "Please specify the location.")

        # Ensure custom_category is filled if "Other" is chosen for category
        if category is None and not custom_category:
            self.add_error("custom_category", "Please specify the category.")

        return cleaned_data
