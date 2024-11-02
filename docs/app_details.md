# blog

The blog app is the main hub of the site so far. Admin can log in and create blog posts.Blog posts are accesible to read for all users. Logged in users can CRUD their own comments. All users can see approved comments. Blogs have a view count which is limited in a session to avoid overcounting.

**Search function**
Users can search through blog posts. TODO can we record searches made by users and/or registered users for future ideas?

# booking

This is currently not wired in. Future uses will be to book discovery calls, book spaces on online masterclasses/lessons/events

# emails

This app is for managing communication with members. It will incorporate features for managing email lists, welcome emails, and tracking:

**Models for Tracking Emails**:

**Newsletter**: A model to store each newsletter or email campaign, including its content, recipients, and send date.

**EmailRecipient**: A model to track each recipient’s engagement with a newsletter (e.g., opens, clicks).

```
from django.db import models
from django.contrib.auth.models import Group, User
from django_summernote.fields import SummernoteTextField

class Newsletter(models.Model):
    title = models.CharField(max_length=255)
    content = SummernoteTextField()
    send_date = models.DateTimeField(auto_now_add=True)
    recipient_groups = models.ManyToManyField(Group)  # Select Django groups as recipients
    # Could include a 'status' field to track whether it has been sent

class EmailRecipient(models.Model):
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opened = models.BooleanField(default=False)
    clicked_links = models.IntegerField(default=0)
    # Add more fields to track engagement as needed
```

**Admin Workflow**:

**Creating a Newsletter**: An admin can log in to the admin panel, create a newsletter using Summernote (for rich text editing), and select recipient groups.

**Selecting Recipient Groups**: By linking the Newsletter model with Django groups, admins can send targeted emails. For example, they can choose to send a newsletter only to the "Testers" group or "Premium Members" group.

**Sending the Newsletter**: After saving the newsletter in the database, you could have a scheduled task (e.g., using Celery) to send it out or trigger an email-sending function when it’s marked as "ready."

**Managing Welcome Emails and Automations**:

**Welcome Emails**: You could set up a signal that sends a welcome email when a new user registers. The emails app can keep a record of this, allowing you to track welcome emails sent and even customize them based on the user’s group.

**Automated Emails**: Using the emails app, you can manage other automated messages, like reminders for subscription renewals, announcements, or responses to specific actions (e.g., signing up for beta access).

**Tracking Engagement:**

**Tracking Opens and Clicks**: As users interact with emails, you can update the EmailRecipient model to track opens or clicks.

**Viewing Engagement in Admin**: You could add custom admin views or reports to see which users/groups are engaging with your emails. This could help you tailor content or follow up with specific groups.

**Future-Proofing for Purchasable Options**:

When we introduce purchasable access to parts of the site, we could create a group for each premium tier (e.g., "Premium Access" or "Special Content") and manage access by adding users to those groups.

We could also use the emails app to send onboarding sequences or special offers to these premium members.

# Linkchecker

This is a small add on, designed to check all links are valid in an email meaage or a website. It didn't function as expected because it's not possible to check hidden links from a "pasted in" email. But it may be useful in our emails model at some point. Not currently wired in.

# LJ Talks

This is the main project level app. It currently houses About Me page, Projects Page, the main sitewide Contact Form

beta aceess is handled in here too but will be moved to the members area.

there is a CustomAccountAdapter in here, not sure what it's for but looks email/contact related?

# member

This app looks after our user profiles. There will be an option to create a profile. Users can manage their comments in here, and can access their purchase history, and manage their newsletter/contact preferences.

members can be assigned to groups for newsletter preferences and special access.

Members could have access to contact form emails they have submitted (and maybe our response)

# Services

This is currentlynot wired in. Defining services became difficult. It was intended for mentoring and coaching services. Abandoned for now.

# ytapi YouTube Channel Checker

This requires special access as it is attached to my google YouTube api key. I should limit this to one or two searches then invite people to add their own api key for personal use. It is accessed by the testers group. Requires a manua application.
