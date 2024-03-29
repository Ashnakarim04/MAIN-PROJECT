# Generated by Django 5.0.3 on 2024-03-18 04:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0147_studentprofile_company_profile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='addaptitude',
            name='applicant',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='website.jobapplication'),
        ),
        migrations.AddField(
            model_name='addaptitude',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
