# Generated by Django 5.0.3 on 2024-03-22 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0166_shortlistedstudent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shortlistedstudent',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.companyprofile'),
        ),
    ]
