from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Stripe Donation
class Donation(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation of {self.amount} at {self.timestamp}"


# Main contact form
class ContactSubmission(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)


# Legal Site Documents
class LegalDocument(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="legal_document")
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)
    # SEO Tags for the blog post
    seo_tags = models.TextField(
        blank=True, help_text="Add your SEO keywords, separated by commas")
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Add short, relevant SEO meta description"
    )

    def __str__(self):
        return self.title
