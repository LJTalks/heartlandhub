# Generated by Django 4.2.13 on 2024-11-19 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0007_remove_business_new_service_area_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='service_area',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]