# Generated by Django 5.0.3 on 2024-03-15 08:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0129_remove_addaptitude_jobb'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionn',
            name='company_profile',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='website.companyprofile'),
        ),
    ]
