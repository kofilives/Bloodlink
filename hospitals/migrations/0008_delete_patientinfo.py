# Generated by Django 5.0.6 on 2024-07-22 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0007_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PatientInfo',
        ),
    ]