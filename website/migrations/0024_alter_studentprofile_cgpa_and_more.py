# Generated by Django 4.2.5 on 2023-10-02 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0023_alter_studentprofile_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='cgpa',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='tenth_cgpa',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='twelfth_cgpa',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='ug_cgpa',
            field=models.FloatField(blank=True, null=True),
        ),
    ]