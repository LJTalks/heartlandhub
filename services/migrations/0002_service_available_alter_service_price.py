# Generated by Django 4.2.16 on 2024-09-15 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='available',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=97.0, max_digits=10),
        ),
    ]
