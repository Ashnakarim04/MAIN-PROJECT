# Generated by Django 5.0.1 on 2024-02-03 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0087_alter_likedcontent_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likedcontent',
            name='status',
            field=models.BooleanField(default=False, verbose_name='status'),
        ),
    ]
