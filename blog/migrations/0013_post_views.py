# Generated by Django 4.2.13 on 2024-10-13 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_comment_updated_on_alter_post_featured_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
