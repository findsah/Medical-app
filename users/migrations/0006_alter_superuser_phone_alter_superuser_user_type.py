# Generated by Django 4.2 on 2023-04-20 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_medicalform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superuser',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=15, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='superuser',
            name='user_type',
            field=models.CharField(choices=[('1', 'Patient'), ('2', 'Doctor')], max_length=2),
        ),
    ]