# Generated by Django 5.0.6 on 2024-07-10 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='firstname',
            field=models.CharField(default='', max_length=50),
        ),
    ]
