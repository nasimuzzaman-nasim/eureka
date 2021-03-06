# Generated by Django 4.0.5 on 2022-06-06 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=55)),
                ('d_type', models.PositiveSmallIntegerField(choices=[(1, 'plain'), (2, 'meter')])),
                ('availability', models.BooleanField()),
                ('needing_repair', models.BooleanField()),
                ('durability', models.PositiveIntegerField()),
                ('max_durability', models.PositiveIntegerField()),
                ('mileage', models.PositiveIntegerField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=14)),
                ('min_rent_period', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
