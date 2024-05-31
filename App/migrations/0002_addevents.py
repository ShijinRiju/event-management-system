# Generated by Django 5.0.2 on 2024-03-02 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddEvents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.IntegerField()),
                ('event', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('country', models.CharField(max_length=100)),
                ('poster', models.ImageField(null=True, upload_to='')),
            ],
        ),
    ]
