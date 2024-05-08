# Generated by Django 4.2.4 on 2023-09-14 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_companyprofile_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='city',
            field=models.CharField(default=' eg: Kochi', max_length=100),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='country',
            field=models.CharField(default=' eg: India', max_length=100),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='district',
            field=models.CharField(default=' eg:Ernakulam', max_length=100),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='pincode',
            field=models.CharField(default=' eg:686403', max_length=15),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='state',
            field=models.CharField(default=' eg:Kerala ', max_length=100),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='website',
            field=models.CharField(default='www.example.com', max_length=100),
        ),
    ]