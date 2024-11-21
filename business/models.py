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


# To determine the area/s the business operates within, admin can update
class ServiceArea(models.Model):
    """
    This model stores all possible service areas.
    Admins can add or update service areas via the admin panel.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# Location Model
class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Business Details
STATUS = ((0, "Draft"), (1, "Published"))


class Business(models.Model):
    """
    This model represents a business listing.
    Each business can choose a pre-defined service area or add a custom one.
    """
    business_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    business_description = models.TextField(blank=True, null=True)
    business_image = CloudinaryField(
        'image', blank=True, null=True,
        default='static/default_business_image.jpg')
    alt_text = models.CharField(
        max_length=255, blank=True, default="Business image")
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    business_category = models.ForeignKey(
        'BusinessCategory', on_delete=models.SET_NULL, blank=True, null=True)
    location = models.CharField(
        max_length=255, blank=True, null=True)  # Free text
    service_area = models.CharField(
        max_length=255, blank=True, null=True)  # Free text
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True,
        related_name="added_businesses")
    is_approved = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS, default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.business_name)
            slug = base_slug
            num = 1
            while Business.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.business_name


class BusinessUpdate(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="updates")
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_data = models.JSONField()  # Store changes in a structured format
    is_reviewed = models.BooleanField(default=False)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def apply_update(self):
        for field, value in self.updated_data.items():
            setattr(self.business, field, value)
        self.business.save()
        self.is_reviewed = True
        self.save()

    def __str__(self):
        return f"Update for {self.business.business_name}"

    class Meta:
        verbose_name_plural = "Businesses"
