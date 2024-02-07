# Generated by Django 4.2.5 on 2023-10-07 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0045_companyprofile_is_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='is_approved',
            field=models.CharField(choices=[('approved', 'Approved'), ('rejected', 'Rejected'), ('pending', 'Pending')], default='pending', max_length=10),
        ),
    ]
