# Generated by Django 5.0.3 on 2024-04-02 19:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0186_interview_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interviews', to='website.studentprofile'),
        ),
    ]
