# Generated by Django 5.0.1 on 2024-02-04 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0089_alter_likedcontent_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='passout',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
