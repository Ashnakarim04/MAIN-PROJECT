# Generated by Django 5.0.3 on 2024-03-16 09:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0144_remove_questionn_company_profile_questionn_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionn',
            name='user',
        ),
        migrations.AddField(
            model_name='questionn',
            name='company_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.companyprofile'),
        ),
    ]