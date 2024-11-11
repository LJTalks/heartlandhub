from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify


# Business category type (update in admin field)
class BusinessCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Business Categories"


# Location Model
class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Business Details

STATUS = ((0, "Draft"), (1, "Published"))


class Business(models.Model):
    # Business Details
    business_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    business_description = models.TextField(blank=True, null=True)
    business_image = CloudinaryField(
        'image', blank=True, null=True, default='static/default_business_image.jpg')

    # Owner/Adder Info
    business_owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name="owned_businesses")
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name="added_businesses")

    #  Should location be limited to a defined list + other?
    LOCATION_CHOICES = [
        ('CityA', 'City A'),
        ('CityB', 'City B'),
        ('Other', 'Other'),
    ]
    location = models.CharField(
        max_length=255, choices=LOCATION_CHOICES, blank=True, null=True)
    custom_location = models.CharField(
        max_length=255, blank=True, null=True, help_text="If 'Other' selected, specify here.")

    # Service area and contact information
    service_area = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # Business category with predefined choices + "Other"
    business_category = models.ForeignKey(
        BusinessCategory, on_delete=models.SET_NULL, blank=True, null=True)
    custom_business_category = models.CharField(
        max_length=100, blank=True, null=True, help_text="If 'Other' selected, specify here.")

    # To track if a business is claimed by the owner, and approval status
    is_claimed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS, default=0)

    # Timestamps
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate initial slug from business name
            base_slug = slugify(self.business_name)
            slug = base_slug
            num = 1
            # Ensure the slug is unique
            while Business.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.business_name

    class Meta:
        verbose_name_plural = "Businesses"


# Business Updates Pending
class PendingBusinessUpdate(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="pending_updates")
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_name = models.CharField(max_length=255, blank=True, null=True)
    updated_description = models.TextField(blank=True, null=True)
    updated_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, blank=True, null=True)
    # Include other fields that can be updated here

    # To track if update has been reviewed
    is_reviewed = models.BooleanField(default=False)

    def apply_update(self):
        """Apply this update to the related business."""
        if self.updated_name:
            self.business.business_name = self.updated_name
        if self.updated_description:
            self.business.business_description = self.updated_description
        if self.updated_location:
            self.business.location = self.updated_location
        # Apply other fields as needed
        self.business.save()
        self.is_reviewed = True
        self.save()
