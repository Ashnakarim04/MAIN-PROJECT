# Generated by Django 5.0.1 on 2024-02-05 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0094_likedcontent1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resume1',
            old_name='stdate',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='resume1',
            old_name='moreinfo',
            new_name='more',
        ),
        migrations.RemoveField(
            model_name='resume1',
            name='caption',
        ),
        migrations.RemoveField(
            model_name='resume1',
            name='certificate',
        ),
    ]
