# Generated by Django 4.0.5 on 2022-06-06 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_min_rent_period_product_minimum_rent_period_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('plain', 'plain'), ('meter', 'meter')], max_length=15),
        ),
    ]
