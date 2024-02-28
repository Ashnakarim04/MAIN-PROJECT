# Generated by Django 5.0.1 on 2024-02-27 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0111_addaptitude_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='AptitudeTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date_and_time', models.DateTimeField()),
                ('duration_minutes', models.IntegerField()),
            ],
        ),
    ]