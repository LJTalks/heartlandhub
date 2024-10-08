# Generated by Django 4.2.16 on 2024-10-07 16:02

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_post_featured_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='publish_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='featured_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
