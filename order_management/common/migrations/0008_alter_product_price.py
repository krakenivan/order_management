# Generated by Django 5.1.5 on 2025-03-04 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(),
        ),
    ]
