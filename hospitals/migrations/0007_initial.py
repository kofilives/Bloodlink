# Generated by Django 5.0.6 on 2024-07-22 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hospitals', '0006_delete_hospital'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ghana_card_id', models.CharField(max_length=15)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=10)),
                ('age', models.IntegerField()),
                ('date_of_birth', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('nationality', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('blood_group', models.CharField(max_length=3)),
                ('has_donated_before', models.BooleanField()),
                ('emergency_contact_name', models.CharField(max_length=100)),
                ('emergency_contact_phone', models.CharField(max_length=15)),
                ('terms_agreed', models.BooleanField(default=False)),
            ],
        ),
    ]
