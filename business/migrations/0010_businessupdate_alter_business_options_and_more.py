# Generated by Django 4.2.13 on 2024-11-21 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0009_servicearea_alter_business_service_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_data', models.JSONField()),
                ('is_reviewed', models.BooleanField(default=False)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Businesses',
            },
        ),
        migrations.AlterModelOptions(
            name='business',
            options={},
        ),
        migrations.RemoveField(
            model_name='business',
            name='business_owner',
        ),
        migrations.RemoveField(
            model_name='business',
            name='custom_business_category',
        ),
        migrations.RemoveField(
            model_name='business',
            name='custom_location',
        ),
        migrations.RemoveField(
            model_name='business',
            name='custom_service_area',
        ),
        migrations.RemoveField(
            model_name='business',
            name='is_claimed',
        ),
        migrations.AlterField(
            model_name='business',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='service_area',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='PendingBusinessUpdate',
        ),
        migrations.AddField(
            model_name='businessupdate',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='business.business'),
        ),
        migrations.AddField(
            model_name='businessupdate',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
