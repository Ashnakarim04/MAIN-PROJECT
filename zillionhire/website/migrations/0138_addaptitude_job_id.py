# Generated by Django 5.0.3 on 2024-03-16 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0137_addaptitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='addaptitude',
            name='job_id',
            field=models.CharField(default='hi', max_length=100),
        ),
    ]
