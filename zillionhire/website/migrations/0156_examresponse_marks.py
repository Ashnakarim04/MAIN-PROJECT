# Generated by Django 5.0.3 on 2024-03-19 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0155_examresponse_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='examresponse',
            name='marks',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]