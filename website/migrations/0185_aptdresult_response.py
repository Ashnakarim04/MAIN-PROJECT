# Generated by Django 5.0.3 on 2024-04-02 18:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0184_alter_aptdresult_student_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='aptdresult',
            name='response',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.examresponse'),
        ),
    ]