# Generated by Django 5.0.1 on 2024-02-05 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0095_rename_stdate_resume1_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resume1',
            old_name='img',
            new_name='image',
        ),
    ]
