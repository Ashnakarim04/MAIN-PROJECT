# Generated by Django 5.0.3 on 2024-03-18 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0152_alter_examresponse_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='addaptitude',
            name='is_approved',
            field=models.CharField(choices=[('approved', 'Approved'), ('rejected', 'Rejected'), ('pending', 'Pending')], default='pending', max_length=10),
        ),
    ]