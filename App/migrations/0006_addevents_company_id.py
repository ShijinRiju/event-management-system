# Generated by Django 5.0.2 on 2024-03-05 07:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0005_companyregister_eventbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='addevents',
            name='company_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.companyregister'),
        ),
    ]
