# Generated by Django 5.0.6 on 2024-07-28 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_appointment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='national_id',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]