# Generated by Django 4.2.13 on 2024-10-11 20:26

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_post_publish_date_alter_post_featured_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='featured_image',
            field=cloudinary.models.CloudinaryField(blank=True, default='placeholder', max_length=255, null=True, verbose_name='image'),
        ),
    ]
