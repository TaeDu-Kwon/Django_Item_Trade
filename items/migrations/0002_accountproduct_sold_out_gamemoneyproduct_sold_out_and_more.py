# Generated by Django 5.1.1 on 2025-01-20 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountproduct',
            name='sold_out',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gamemoneyproduct',
            name='sold_out',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='itemproduct',
            name='sold_out',
            field=models.BooleanField(default=False),
        ),
    ]
