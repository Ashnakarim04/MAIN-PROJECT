# Generated by Django 5.0.1 on 2024-02-04 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0090_studentprofile_passout'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentprofile',
            old_name='passout',
            new_name='passout_year',
        ),
    ]